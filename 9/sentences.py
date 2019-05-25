import os
import re

class Sentences(object):
    def __init__(self,filename):
        self.filename = filename
    def __iter__(self):
        with open(self.filename) as phrases:
            for line in phrases:
                yield line.rstrip("\n").split("\t")[:-1]
