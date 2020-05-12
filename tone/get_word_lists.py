import requests

base_url = "http://www3.nd.edu/~mcdonald/Data/Finance_Word_Lists"

url  = ("LoughranMcDonald_Positive.csv",
                   "LoughranMcDonald_Negative.csv",
                   "LoughranMcDonald_Uncertainty.csv",
                   "LoughranMcDonald_Litigious.csv",
                   "LoughranMcDonald_ModalStrong.csv",
                   "LoughranMcDonald_ModalWeak.csv")

category = ("positive", "negative", "uncertainty",
            "litigious", "modal_strong", "modal_weak")


def get_words(i):
    r = requests.post(base_url + '/' + url[i])
    if r.ok:
        data = r.content.decode('utf8')
        word_list = data.split('\r\n')
        return [word.lower() for word in word_list if word != '']

word_lists = { cat: get_words(i) for i, cat in enumerate(category) }

# Save dictionary as text file
f = open("tone/word_lists.py", "w")
f.write("word_lists = " + str(word_lists))
f.close()
