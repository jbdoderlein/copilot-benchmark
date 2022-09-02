import os
import re
import math

import pandas as pd

import enchant

d = enchant.Dict("en_US")

original_path = "humaneval/prompts/original"

regex = r"(\"\"\")(.*)(\"\"\")"

def check_bad_char(text:str) -> str:
    bad_chars = [">>>", "<=", "[", "==>", "#", "=>", "➞","->"]
    for char in bad_chars:
        if char in text:
            return True

def clean(text:str) -> str:
    cleaned = [".", ",", "(", ")", "'", '"', ":", "*"]
    for char in cleaned:
        text = text.replace(char, "")
    return text

def is_a_number(text:str) -> bool:
    try:
        float(text)
        return True
    except ValueError:
        return False

word_file = {}
word_set = set()

for i, f in enumerate(os.listdir(original_path)):
    if os.path.isfile(os.path.join(original_path, f)):
        with open(os.path.join(original_path, f),'r') as f2:
            content = f2.read()
        matches = re.finditer(regex, content, re.MULTILINE | re.DOTALL)
        for match in matches:
            comment = clean(match.group()[3:-3])
        words = []
        for line in comment.strip().split("\n"):
            if not check_bad_char(line):
                for i in line.split():
                    if d.check(i) and (not is_a_number(i)):
                        words.append(i.lower())
        word_file[f] = words
        word_set.update(words)
        

number_of_doc_term = {i:0 for i in word_set}


tf_files = {}
tf_idf_files = {}

for file, content in word_file.items():
    tf_vect = {}
    for word in word_set:
        tf_vect[word] = content.count(word) / len(content)
        if tf_vect[word] > 0:
            number_of_doc_term[word] += 1
    tf_files[file] = tf_vect

idf_words = {word:math.log(len(word_file) / number_of_doc_term[word]) for word in word_set}

for file, tf_vect in tf_files.items():
    tf_idf_vect = {}
    for word, tf in tf_vect.items():
        tf_idf_vect[word] = tf * idf_words[word]
    tf_idf_files[file] = tf_idf_vect


df = pd.DataFrame(tf_idf_files)
print(df)
df.to_csv("tf_idf.csv")
