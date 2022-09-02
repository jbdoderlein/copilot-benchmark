"""List of utilities for transforming code and docstrings."""
import re
import requests
import random

from flair.data import Sentence
from flair.models import SequenceTagger
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline

import pandas as pd


def extract_docstring(text):
    """
    Extract the docstring from Humal code.
    """
    regex = r"(\"\"\")(.*)(\"\"\")"
    # Split content
    rev = text.split('"""')
    if len(rev) > 3:
        after = '"""'.join(rev[-3:])
    else:
        after = text
    matches = re.finditer(regex, after, re.MULTILINE | re.DOTALL)
    for match in matches:
        return match.group()[3:-3]

def extract_defline(code):
    """
    Given a full Human code return the last def line.
    """
    lines = code.split('\n')
    for line in reversed(lines):
        if line.strip().startswith('def '):
            return line.strip()
    return None

def init_ml_model():
    """
    Initialize a machine learning model.
    return: model, pipeline, tagger
    """
    unmasker = pipeline('fill-mask', model='bert-base-uncased')
    # load tagger
    tagger = SequenceTagger.load("flair/pos-english")
    #Load the model
    model = SentenceTransformer('sentence-transformers/msmarco-distilbert-cos-v5')
    return model, unmasker, tagger


def find_verb(text, tagger):
    """
    Find the first verb in a sentence.
    """
    sentence = Sentence(text)
    # predict NER tags
    tagger.predict(sentence)

    for label in sentence.get_labels():
        if label.value in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'MD']:
            return label.data_point.form

def cosine_similarity(query, docs, model):
    """
    Return the document with maximum cosine similarity between a query and a list of documents.
    """
    #Encode query and documents
    query_emb = model.encode(query)
    doc_emb = model.encode(docs)

    #Compute dot score between query and all document embeddings
    scores = util.cos_sim(query_emb, doc_emb)[0].cpu().tolist()

    #Combine docs & scores
    doc_score_pairs = list(zip(docs, scores))

    #Sort by decreasing score
    doc_score_pairs = sorted(doc_score_pairs, key=lambda x: x[1], reverse=True)

    #Output passages & scores
    for doc, _ in doc_score_pairs:
        return doc


def get_alternatives(text, unmasker, tagger):
    """
    Get list of possible alternatives for a given text.
    """
    verb = find_verb(text, tagger)
    if verb is None:
        return []
    masked = text.replace(f"{verb} " , '[MASK]', 1)
    if not 'MASK' in masked:
        return []
    pos = unmasker(masked)
    return [text.replace(verb, p['token_str'], 1) for p in pos 
                if p['score']>0.01 and p['token_str'] != verb]


def cat(code):
    """
    Given a full Human code (no_example), return the code witt tha CAT transform.
    """
    model, unmasker, tagger = init_ml_model()
    docstring = extract_docstring(code)
    phrases = docstring.split('.')
    final = []
    for phrase in phrases:
        alternatives = get_alternatives(phrase, unmasker, tagger)
        if len(alternatives) > 0:
            sim = cosine_similarity(phrase, alternatives, model)
            final.append(sim.capitalize())
        else:
            final.append(phrase)

    return code.replace(docstring, '.\n    '.join(final)+'.\n    ')

def translate(code, auth_key):
    """
    Given a full Human code return the code with french docstring.
    """
    docstring = extract_docstring(code)
    deepl = requests.post(
                "https://api-free.deepl.com/v2/translate",
                data={
                    "auth_key": auth_key,
                    "text" : docstring,
                    "target_lang" : "FR"},
            )
    return code.replace(docstring, deepl.json()["translations"][0]["text"])

def keyword_cut(file_name, code, cut, path="tf_idf.csv"):
    """
    Given a full Human code return the code with a number of words cut.
    """
    docstring = extract_docstring(code)
    tfidf = pd.read_csv(path, index_col=0)

    vector = tfidf[file_name].sort_values(ascending=True)
    vector = vector.drop(vector[vector == 0.0].index) #  Drop word not in prompt
    numb = int(len(vector) * cut)
    replacement = vector.index.tolist()[:numb]
    new_docstring = docstring
    for word in replacement:
        new_docstring = new_docstring.replace(f" {word} ", " ")
    return code.replace(docstring, new_docstring)

def mask_signature(code, name=True, args=True):
    """
    Given a full Human code return the code with a signature mask.
    """
    ALPHABET = list('abcdefghijklmnopqrstuvwxyz')
    def_line = extract_defline(code)

    if name:
        fname = ''.join(random.sample(ALPHABET,8))
    else:
        fname = def_line.split('(')[0].split('def ')[1]
    
    if args:
        narg = len(def_line.split('(')[1].split(')')[0].split(','))
        fargs = ', '.join([''.join(random.sample(ALPHABET,8)) for _ in range(narg)])
    else:
        fargs = def_line.split('(')[1].split(')')[0]
    
    new_signature = f"def {fname}({fargs}):"
    return code.replace(def_line, new_signature)
