from abc import ABC, abstractmethod
import string

class Tokenizer(ABC):
    @abstractmethod
    def tokenize(self,text:str)->list:
        pass


class TokenizerSimple(Tokenizer):
    def tokenize(self, text:str)->list:
        text = text.translate(text.maketrans('', '', string.punctuation))
        text = text.lower()
        return text.split()