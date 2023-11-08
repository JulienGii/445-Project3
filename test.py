import os
import json
from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import nltk


###
# # create an empty list
# l = []
# print(str(stopwords.words('english')))

###
# def create_stopwords_list():
#     # retrieve the list from nltk
#     stopword = stopwords.words('english')
    
#     stemmer = PorterStemmer()
#     tokens = []
#     for w in stopword:
#         tokens.append(stemmer.stem(nltk.word_tokenize(w)[0]))
#     return set(tokens)



# l = create_stopwords_list()
# print(len(l))

###
l = [('a', 5), ('a', 5)]
s = set(l)
print(l)
print(s)