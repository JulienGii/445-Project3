# NOTE Working version. 
import json
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import os
from bs4 import BeautifulSoup
import sys

# General function
def greeting():
    print('*********************\nHow many files do you want to process?')
    return int(input('Enter a number between 1 and 21\n'))


def output_to_txt(output_dir: str, pipeline_name: str, sgm_file_number: int, output):
    # create filename
    filename = os.path.join(output_dir + pipeline_name +
                            '(' + str(sgm_file_number) + ')' + '.txt')
    f = open(filename, 'w')
    if isinstance(output, str):
        f.write(output)
    elif isinstance(output, list):
        for e in output:
            f.write(str(e) + '\n')
    elif isinstance(output, dict):
        # for key, value in output.items():
        #     f.write(str(key) + ' : ' + str(value))
        f.write(json.dumps(output, indent=4))


    f.close()
    print(filename + ': Success')


# STEP 1: Helper functions
# takes the output directory name and creates it if it does not already exist
def create_output_directory(output_directory_name: str):
    try:
        os.mkdir(path=output_directory_name)
        print("Output directory created")
    except FileExistsError:
        pass


# TODO remove whole thing
# takes a directory and a number of sgm file to retrieve, outputs a list of closed sgm files
def retrieve_files(directory, num_to_retrieve):
    print("Retrieving files")
    num_file = 0
    files = []
    for file in os.listdir(directory):
        if num_file >= num_to_retrieve:
            break
        if not file.endswith(".sgm"):
            continue
        filename = os.path.join(directory, file)
        files.append(filename)
        num_file += 1

    return files

 

# takes an sgm_file and outputs a dict of strings. Each string is the raw texts (title and bodie) of one news article, the key is the docID
def extract_raw_text(sgm_file):
    # documents is a docId : raw_text dictionary 
    documents = {}
    docId = 0
    soup = BeautifulSoup(sgm_file, 'html.parser')
    file_contents = soup.find_all("reuters")
    for content in file_contents:
        title = content.find("title")
        title = title.text if title else ""
        body = content.find("body")
        body = body.text if body else ""
        # form a text
        text = title + " " + body
        documents[docId] = text
        docId += 1
    return documents


# STEP 1: Actual function
def read_and_extract(sgm_file):
    raw_text = []
    # f = open(sgm_file.name, 'r')
    f = open(sgm_file, 'r')
    raw_text = extract_raw_text(f) # raw_text is a dict
    f.close()
    return raw_text


#  STEP 2:
# input is a list of strings
# outputs a list of tokenized texts
def tokenize(raw_text):
    counter = 1
    tokenized_text = []
    for docId, text in raw_text.items():
        tokens = []
        for word in nltk.word_tokenize(text):
            word = ''.join(e for e in word if word.isalnum())
            if not word:
                continue
            tokens.append(word)
        tokenized_text.append((docId, tokens))
    counter += 1

    return tokenized_text


# Step 3:
# input is a list of string
# output list of lowercase strings

def lowercase(tokens):
    counter = 1
    lowercased_tokens = []
    for docId, tokens in tokens:
        lowercases = []
        for token in tokens:
            lowercases.append(str(token).lower())
        lowercased_tokens.append((docId, lowercases))
        counter += 1
    return lowercased_tokens

# Step 4:
# input is list of string
# output is list of stemmed strings
def porter_stemmer(str_list):
    stemmer = PorterStemmer()
    counter = 1
    stemmed_tokens = []
    for docId, tokens in str_list:
        stemmed = []    
        for token in tokens:
            stemmed.append(stemmer.stem(token))
        stemmed_tokens.append((docId, stemmed))

        counter += 1
    return stemmed_tokens

def create_stopwords_list():
    # retrieve the list from nltk
    stopword = stopwords.words('english')
    
    stemmer = PorterStemmer()
    tokens = []
    for w in stopword:
        tokens.append(stemmer.stem(nltk.word_tokenize(w)[0]))
    return set(tokens)
        
def remove_stopwords(stopwords, tokens):
    documents = []
    for docId, tokens in tokens:
        tokens_without_stopwords = []
        for w in tokens:
            if w not in stopwords:
                tokens_without_stopwords.append(w)
        documents.append((docId, tokens_without_stopwords))
    return documents


# Constant initialization
CORPUS_DIRECTORY = "Reuters-21578"
OUTPUT_DIRECTORY = "OutputsScript2/"
NUM_FILES_TO_RETRIEVE = greeting()


def pipeline():
    create_output_directory(OUTPUT_DIRECTORY)
    sgm_files = retrieve_files(directory=CORPUS_DIRECTORY, num_to_retrieve=NUM_FILES_TO_RETRIEVE)
    file_num = 1
    for file in sgm_files:
        raw_text = read_and_extract(file)
        output_to_txt(OUTPUT_DIRECTORY, 'read_and_extract', file_num, raw_text)
        tokenized_texts = tokenize(raw_text)
        output_to_txt(OUTPUT_DIRECTORY, 'Tokenizer-output', file_num, tokenized_texts)
        lowercased = lowercase(tokenized_texts)
        output_to_txt(OUTPUT_DIRECTORY, 'Lowercased-output', file_num, lowercased)
        stemmed = porter_stemmer(lowercased)
        output_to_txt(OUTPUT_DIRECTORY, 'Stemmed-output', file_num, stemmed)
        no_stopwords = remove_stopwords(create_stopwords_list(), stemmed)
        output_to_txt(OUTPUT_DIRECTORY, 'No-Stopword-output', file_num, no_stopwords)
        file_num += 1


pipeline()
