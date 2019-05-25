#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  7 10:41:09 2018

@author: marcin
"""

import WNQuery
log = open("parse_file.log","w+")
#3
query = WNQuery.WNQuery("plwordnet-3.1-visdisc.xml",log)
log.close()

def getSynset(literal,sense):
     synsets = query.lookUpLiteral(literal,"n")
     if synsets == []: 
          synsets = query.lookUpLiteral(literal,"a")
     for synset in synsets:
          for synonym in synset.synonyms:
               if synonym.literal == literal and synonym.sense == sense:
                    return synset
     raise Exception("None of synsets have literal: {} with sense: {}".format(literal,sense))
     
def getRelation(synset1,synset2,literal1,literal2):
     if synset1.wnid == synset2.wnid:
          return "{} belongs to the same synset as {}".format(literal1,literal2)
     for relation in synset1.ilrs:
          if(relation[0] == synset2.wnid):
               return "{} -- {} --> {}".format(literal1,relation[1],literal2)
     return "{} not related to {}".format(literal1,literal2)  
     
szkody = query.lookUpLiteral("szkoda","n")

for szkoda in szkody: print("{}\n".format(szkoda))

print(query.lookUpID("PLWN-00418091-j","a"))

#szkoda1
#definition: brak danych
#domain: msc => miejsca i umiejscowienie
#Usages([ziemia w gospodarstwie zniszczona przez zwierzęta])

#szkoda2
# domain: zdarz => zdarzenia
#Synonym(strata1, utrata1, szkoda2, uszczerbek1)


def getAllDescendants(synset,relation):
     result = []
     for relative in synset.ilrs:
          if relative[1] == relation:
               s = query.lookUpID(relative[0],"n")
               print(s)
               result.append((synset,s))
               result.extend(getAllDescendants(s,relation))
     return result

           
#4
wypadek_drogowy = query.lookUpLiteral("wypadek drogowy","n")
result = getAllDescendants(wypadek_drogowy[0],"hypernym")

print(wypadek_drogowy)
wypadek_drogowy_hyper_1 = query.lookUpID("PLWN-00410901-n","n")
wypadek_drogowy_hyper_2 = query.lookUpID("PLWN-00324365-n_pwn","n")
print(wypadek_drogowy_hyper_1)
print(wypadek_drogowy_hyper_2)

#5 wypadek1 PLWN-00003982-n
wypadki = query.lookUpLiteral("wypadek","n")


wypadek_hiponimy_1_rzedu = []
print("###########################################################################################")
print("HIPONIMY I RZĘDU DLA RZECZOWNIKA WYPADEK1")
print("###########################################################################################")
for relacja in wypadki[1].ilrs:
     if relacja[1] == "hiponimia" or relacja[1] == "hyponym":
          wypadek_hiponimy_1_rzedu.append(relacja[0])
          res = query.lookUpID(relacja[0],"n")
          for synonym in res.synonyms:
               print("{}_{}".format(synonym.literal,synonym.sense))
#6      
wypadek_hiponimy_2_rzedu = set()
for hiponim in wypadek_hiponimy_1_rzedu:
     print(hiponim)
     synset = query.lookUpID(hiponim,"n")
     for relacja in synset.ilrs:
        print(relacja)
        if relacja[1] == "hiponimia" or relacja[1] == "hyponym":  
             res = query.lookUpID(relacja[0],"n")
             for synonym in res.synonyms:
                  wypadek_hiponimy_2_rzedu.add("{}_{}".format(synonym.literal,synonym.sense))
     print()
print("###########################################################################################")
print("HIPONIMY 2 RZĘDU DLA RZECZOWNIKA WYPADEK1")
print("###########################################################################################")
for res in wypadek_hiponimy_2_rzedu:
     print(res)
#7
#I
lexems1 = [
          ("szkoda","2"),("strata","1"),("uszczerbek","1"),
          ("szkoda majątkowa","1"),("uszczerbek na zdrowiu","1"),
          ("krzywda","1"),("niesprawiedliwość","1"),("nieszczęście","2")
          ]
synsets1 = []
for lexem in lexems1:
     synsets1.append((getSynset(lexem[0],lexem[1]),"{}_{}".format(lexem[0],lexem[1])))   

   
for s1 in synsets1:
     for s2 in synsets1:
          if(s1 == s2): continue
          print(getRelation(s1[0],s2[0],s1[1],s2[1]))


print(getSynset("bezkolizyjny","2"))
lexems2 = [
          ("wypadek","1"),("wypadek komunikacyjny","1"),("kolizja","2"),
          ("zderzenie","2"),("kolizja drogowa","1"),
          ("bezkolizyjny","2"),("katastrofa budowlana","1"),("wypadek drogowy","1")
          ]

synsets2 = []
for lexem in lexems2:
     synsets2.append((getSynset(lexem[0],lexem[1]),"{}_{}".format(lexem[0],lexem[1])))   

   
for s1 in synsets2:
     for s2 in synsets2:
          if(s1 == s2): continue
          print(getRelation(s1[0],s2[0],s1[1],s2[1]))
          
          
#8
szkoda2 = getSynset("szkoda","2")
print(szkoda2)
wypadek1 = getSynset("wypadek","1")
print(wypadek1)
kolizja2 = getSynset("kolizja","2")
print(kolizja2)
szkoda_majatkowa1 = getSynset("szkoda majątkowa","1")
print(szkoda_majatkowa1)

nieszczescie2 = getSynset("nieszczęście","2")
print(nieszczescie2)
katastrofa_budowlana1 = getSynset("katastrofa budowlana","1")

print("{}: ({}, {})".format(query.simLeaCho(szkoda2.wnid,wypadek1.wnid,"n","hyponym",False),szkoda2.wnid,wypadek1.wnid))
print("{}: ({}, {})".format(query.simLeaCho(kolizja2.wnid,szkoda_majatkowa1.wnid,"n","hyponym",False),kolizja2.wnid,szkoda_majatkowa1.wnid))
print("{}: ({}, {})".format(query.simLeaCho(nieszczescie2.wnid,katastrofa_budowlana1.wnid,"n","hyponym",False),nieszczescie2.wnid,katastrofa_budowlana1.wnid))

print(query.similarityLeacockChodorow("szkoda","wypadek","n","hiponimia",True))
print(query.similarityLeacockChodorow("kolizja","szkoda majątkowa","n","hiponimia",True))
print(query.similarityLeacockChodorow("nieszczęście","katastrofa budowlana","n","hiponimia",True))




##################################################################################################
max = 0
for symset in query.dat("n"):
     path_length = query.getMaxDepth(symset,"n","hiponimia")
     if path_length > max:
          max = path_length
          print(max)



