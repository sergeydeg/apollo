from functools import reduce
import operator

import yaml


class Translate:

    def __init__(self):
        with open('locales/en.yml', 'r') as f:
            self.en = yaml.load(f)


    def __call__(self, entry):
        return reduce(operator.getitem, entry.split("."), self.en)


t = Translate()
