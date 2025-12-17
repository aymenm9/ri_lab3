import string
import nltk
from nltk.corpus import stopwords
import re
from nltk.stem import PorterStemmer
from tokenizers import Tokenizer


class Preprocessor:
    def __init__(self, tokenizer:Tokenizer, stemmer:PorterStemmer, stop_words:set = None):
        self.tokenizer = tokenizer
        self.stemmer = stemmer
        if stop_words is None:
            nltk.download('stopwords')
            self.stop_words = set(stopwords.words('english'))
        else:
            self.stop_words = stop_words
    def pre_process(self, text:str):
        tokens = self.tokenizer.tokenize(text)
        tokens = [token for token in tokens if token not in self.stop_words] # remove stop words
        tokens = [self.stemmer.stem(token) for token in tokens] # stem tokens
        return tokens
    