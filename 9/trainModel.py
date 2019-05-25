from gensim.models.phrases import Phraser, Phrases
from documents import Documents
from sentences import Sentences
from gensim.models import Word2Vec
import os


# resultDir='/home/marcin/Documents/AGH/PJN/data/json/word2vec/'
data_dir = "/home/marcin/Documents/AGH/PJN/data/json/word2vec/new"
# #
# print("finding 3-word phrases")
documents = Documents(data_dir)

bigram = Phraser(Phrases(documents))
trigram = Phraser(Phrases(bigram[documents]))
sentences = open(os.path.join(data_dir,"sentences-3.txt"),"w+")
print("saving sentences to file")
for s in trigram[bigram[documents]]:
     for sentece in s:
         sentences.write("{}\t".format(sentece))
     sentences.write("\n")
sentences.close()


# trigram = Phraser(Phrases(bigram[sentences]))

#trigram = Phraser.load(os.path.join(data_dir,"phrases"))

sentences = Sentences(os.path.join(data_dir,"sentences-3.txt"))
#
# print("training model")
# model = Word2Vec(sentences=sentences,window=5,min_count=3,sg=0,size=300)
# model.save(os.path.join(data_dir,"word2vec_model"))
#
model = Word2Vec.load(os.path.join(data_dir,"word2vec_model"))
# #
print(model.wv.most_similar("kpk"))

# res = open("senteces.txt","w+")
# for sentences in trigram[sentences]:
#     for sentence in sentences:
#         res.write(sentence)
#         res.write("\n")
# res.close()
#
# model = Word2Vec(trigram)
# model.save(os.path.join("model"))
