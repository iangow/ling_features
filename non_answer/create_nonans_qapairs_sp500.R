# 接着干 This code removes the duplicated call records from two sources
library(dplyr, warn.conflicts = FALSE)
library(DBI)
pg <- dbConnect(RPostgres::Postgres())
rs <- dbExecute(pg, "SET search_path TO yiyangw2")
rs <- dbExecute(pg, "SET work_mem TO '30GB'")


qa_pairs_sp500 <- tbl(pg, "qa_pairs_sp500") %>%
  filter(section == 1) %>% compute() # 965628/966044

non_answers_wu_sp500 <- tbl(pg, "non_answers_wu_sp500")%>%
  filter(section == 1) %>% compute() # 154638/154769

regexes <-tbl(pg, "regexes") %>% compute()

qa_pairs_sp500 <- qa_pairs_sp500 %>%    
  mutate(speaker_number_ques = unnest(question_nums)) %>%
  mutate(speaker_number_ans = unnest(answer_nums)) %>% # suggested mutate step by step
  distinct() %>%
  compute()

non_answers <- non_answers_wu_sp500 %>%
  distinct() %>%
  mutate(has_non_answer = !is.na(non_answers)) %>%
  mutate(non_answer = sql("unnest(non_answers)")) %>%
  mutate(regex_id = sql("(non_answer->'regex_id')::text::integer")) %>%
  left_join(regexes, by = "regex_id") %>%
  filter(!is.na(category)) %>%
  group_by(file_name, last_update, speaker_number) %>%
  summarise(is_refuse = bool_or(category == 'REFUSE'),
            is_unable = bool_or(category == 'UNABLE'),
            is_aftercall = bool_or(category == 'AFTERCALL')) %>%
  ungroup() %>%
  mutate(is_nonans = is_refuse | is_unable | is_aftercall) %>% distinct() %>%
  compute()

non_answers %>% head(1)
# rs <- dbExecute(pg, "SET search_path TO streetevents")
# text <- tbl(pg, "speaker_data") %>%
#   filter(section == 1 & context == "qa") %>% compute()
qa_pairs_sp500 %>% head(1)

qa_non_answer <- qa_pairs_sp500 %>% select (-section) %>% 
  left_join(non_answers, by = c("speaker_number_ans" = "speaker_number", "file_name" = "file_name",
                                "last_update" = "last_update")) %>% 
  left_join(non_answers, by = c("speaker_number_ques" = "speaker_number", "file_name" = "file_name",
                                                  "last_update" = "last_update")) %>% 
  select(-is_unable.y, -is_refuse.y, -is_nonans.y, -is_aftercall.y) %>%
  rename(is_unable = is_unable.x, is_refuse = is_refuse.x, is_aftercall=is_aftercall.x, is_nonans=is_nonans.x ) %>%
  compute(name = "nonans_qapairs", temporary = FALSE)


rs <- dbExecute(pg, "ALTER TABLE nonans_qapairs rename to nonans_qapairs_sp500")
rs <- dbExecute(pg, "GRANT SELECT ON TABLE nonans_qapairs_sp500 TO yiyangw2")
rs <- dbExecute(pg, "CREATE INDEX ON nonans_qapairs_sp500 (file_name,last_update,answer_nums, question_nums)")

comment <- 'CREATED USING yiyangw2/non_answers/create_nonans_qapairs_sp500.R'
sql <- paste0("COMMENT ON TABLE nonans_qapairs_sp500 IS '",
              comment, " ON ", Sys.time() , "'")
rs <- dbExecute(pg, sql)

dbDisconnect(pg)



