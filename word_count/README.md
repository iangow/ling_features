## Creating linguistic data

#### Overview

| Data                 | Main Code           |Supplementary Codes                | Output table          | Primary key |
| :-------------       |:-------------:      |:-------------:             | :-----                | :------
| Word counts   | `word_count_run.py` | `word_count_add.py`, `word_count_functions.py` | `se_features.word_counts` | `(file_name, last_update, section, context, speaker_name)` |

Note that the code is designed to run in an incremental fashion. 
The code first examines which calls are available that are not found in the output table and only processes those calls.
So the code below can be run to update tables after updating StreetEvents.

#### Running word count code.

Run the code below in console from the `liwc_etc` directory.
```bash
export PGHOST="some_host.edu"
export PGDATABASE="db_name"
./word_count_run.py
```
The code will take files from `streetevents.calls` and find word counts for corresponding `speaker_text` data in `streetevents.speaker_data`.
By default, results will be saved in `se_features.word_counts`

(Specify `output_schema` and `output_table` in  `word_count_run.py` to change the output table. 
Specify `num_files` in `word_count_run.py` to run the code for a limited number of files for testing purposes.)