import glob
import os
import re
import json

class Documents(object):
    def __init__(self,dirname):
        self.dirname = dirname
    def __iter__(self):
        for fname in glob.glob(os.path.join(self.dirname,"*.json")):
            judgements = json.load(open(fname));
            for item in judgements["items"]:
                yield self.words(self.delete_html_tags(self.delete_broken_words(item['textContent'])))

    def delete_html_tags(self,text):
        return re.sub(r'<[^>]*>', '', text)

    def delete_broken_words(self,text):
        return re.sub(r'-\n', '', text)

    def words(self,text): return re.findall(r'\w+', text.lower(),re.UNICODE);