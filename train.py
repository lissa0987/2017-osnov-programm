import re
import nltk

a = open('wiki.txt', 'r')
text = ''

for i in a.readlines():
    text += i
print(type(text))
tokens = nltk.word_tokenize(text)
print(tokens)


with open('tokens.txt', 'r', encoding='utf-8') as file:
    tags = {}
    letter = ''
    punct = ['.', ',', '?', '!', '"', '„', '“', '„', '“', ':', "(", "—"]
    #for i in file.readlines():
        #print(i)
    for u in file:
        no_frequency = u[9:]
        tag_text = no_frequency.split('/')
        if len(tag_text) != 1:

            if tag_text[1][0:2] == "NN" or tag_text[1][0:2] == "Ve" or tag_text[1][0:2] == "AU":
                tag_text[1] = "NOUN"

            elif tag_text[1][0:2] == "AA" or tag_text[1][0:2] == "Dg":
                tag_text[1] = "ADJ"

            elif tag_text[1][0:2] == "Vf" or tag_text[1][0:2] == "Vp" or tag_text[1][0:2] == "Vc" or tag_text[1][0:2] == "VB" or tag_text[1][0:2] == "Vs":
                tag_text[1] = "VERB"
            elif tag_text[1][0] == "C":
                tag_text[1] = "NUM"
            elif tag_text[1][0:2] == "C" or tag_text[1][0:2] == "Cl" or tag_text[1][0:2] == "Cr" or tag_text[1][0:2] == "Cn" or tag_text[1][0:2] == "Ch":
                tag_text[1] = "NUM"
            elif tag_text[1][0:2] == "PR":
                tag_text[1] = "ADP"
            elif tag_text[1][0] == "J":
                tag_text[1] = "CCONJ"
            elif tag_text[1][0:2] == "RR" or tag_text[1][0:2] == "PR" or tag_text[1][0:2] == "RV":
                tag_text[1] = "PREP"
            elif tag_text[1][0:2] == "PL" or tag_text[1][0:2] == "P7" or tag_text[1][0:2] == "TT" or tag_text[1][0:2] == "PE" or tag_text[1][0:2] == "PP":
                tag_text[1] = "PRON"
            elif tag_text[1][0:2] == "Db":
                tag_text[1] = "ADV"
            elif tag_text[1][0:2] == "P4" or tag_text[1][0:2] == "P1" or tag_text[1][0:2] == "PL" or tag_text[1][0:2] == "PD" or tag_text[1][0:2] == "P5":
                tag_text[1] = "DET"

            else:
                tag_text[1] = "X"
              
            letter = re.sub(r'[^a-žA-Ž0-9]', '', tag_text[0])
            tags[letter] = tag_text[1]

tags["."] = "PUNCT"
tags[","] = "PUNCT"
tags["?"] = "PUNCT"
tags["()"] = "PUNCT"
tags['""'] = "PUNCT"
tags["!"] = "PUNCT"
tags[","] = "PUNCT"
tags["„“"] = "PUNCT"
tags[":"] = "PUNCT"
tags["—"] = "PUNCT"
print(tags)
print(len(tags))

tags_amount = 0
tags_and_tokens = {}
for i in tags:
    for u in range(len(tokens)):
        if i == tokens[u]:
            tags_and_tokens[tokens[u]] = tags[i]
print(tags_and_tokens)

words = len(tags_and_tokens)
tags_amount = {}
words_amount = {}
count = 0

for i in tags_and_tokens: 
    tags_amount[tags[i]] = tags_amount.get(tags[i],0) + 1
for i in tags_and_tokens: 
    if i not in words_amount:
        words_amount[i] = 1
    else:
        word_amount[i] += 1
print(words_amount)
name= input()
f = open(name, 'w')
f.write('#P' + '\t' + 'count' + '\t' + 'tag' + '\t' + 'form' + '\n')
words_am = len(tokens)
for i in tags_amount: 
    p = tags_amount[i]/words
    #a = int(p)
    f.write(str(p)) 
    f.write('\t' + str(tags_amount[i]) + '\t' + i + '\t' + '-' + '\n')
for i in words_amount:
    p = words_amount[i]/words
    f.write(str(p)) 
    f.write('\t' + str(words_amount[i]) + '\t' + tags_and_tokens[i] + '\t' + i + '\n')   

f.close()
    
                

