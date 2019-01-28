from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from typing import Text

from pythainlp.tokenize import word_tokenize
from rasa_nlu.components import Component
from rasa_nlu.tokenizers import Token


class LextoTokenizer(Component):
    """
    Requires:
    1. PyThaiNLP
    2. sklearn_crfsuite
    pip install https://github.com/PyThaiNLP/pythainlp/archive/dev.zip
    pip install sklearn_crfsuite
    """
    name = "tokenizer_pylexto"
    provides = ["tokens"]

    def __init__(self, component_config=None):
        super().__init__(component_config)

    def process(self, message, **kwargs) -> None:
        message.set("tokens", self.tokenize(message.text))

    def train(self, training_data, config, **kwargs):
        for example in training_data.training_examples:
            example.set("tokens", self.tokenize(example.text))

    def tokenize(self, text: Text):
        tmp = word_tokenize(text, engine='pylexto')
        words = [elem for elem in tmp if elem.strip()]

        running_offset = 0
        tokens = []
        for word in words:
            word_offset = text.index(word, running_offset)
            word_len = len(word)
            running_offset = word_offset + word_len
            tokens.append(Token(word, word_offset))
        return tokens
