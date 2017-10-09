# -*- coding: utf-8 -*-

import re
import sys
#here the vocab was created.
'''f = open('transl.txt', 'w')

transliteration = {}
transliteration["Á"] = 'АА'
transliteration["A"] = 'А'
transliteration["B"] = 'Б'
transliteration["C"] = 'Ц'
transliteration["Č"] = 'Ч'
transliteration["D"] = 'Д'
transliteration["Ď"] = "Д'"
transliteration["E"] = 'Э'
transliteration["É"] = 'ЕЕ'
transliteration["Ě"] = 'Е'
transliteration["F"] = 'Ф'
transliteration["G"] = 'Г'
transliteration["N"] = 'Н'
transliteration["CH"] = 'Ч'
transliteration["I"] = 'И'
transliteration["Í"] = 'ИИ'
transliteration["J"] = 'Й'
transliteration["K"] = 'К'
transliteration["L"] = 'Л'
transliteration["M"] = 'М'
transliteration["N"] = 'Н'
transliteration["Ň"] = "Н'"
transliteration["O"] = 'О'
transliteration["Ó"] = 'OO'
transliteration["P"] = 'П'
transliteration["Q"] = 'КВ'
transliteration["R"] = 'Р'
transliteration["Ř"] = 'RZH'
transliteration["S"] = 'С'
transliteration["Š"] = 'Ш'
transliteration["T"] = 'Т'
transliteration["Ť"] = "T'"
transliteration["U"] = 'У'
transliteration["Ú"] = 'УУ'
transliteration["Ů"] = 'ОУ'
transliteration["V"] = 'В'
transliteration["W"] = 'В'
transliteration["X"] = 'КС'
transliteration["Y"] = 'Ы'
transliteration["Ý"] = 'ЫЫ'
transliteration["Z"] = 'З'
transliteration["Ž"] = 'Ж'

for i in transliteration:
    f.write(i)

    f.write('\t')
    f.write(transliteration[i])
    f.write('\n')
    f.write(i.lower())
    f.write('\t')
    f.write(transliteration[i].lower())
    f.write('\n')
f.close()'''



punct = ['.', ',', '?', '!', '„', ':', "(", "—"]
sign = ''
list_of_sign = []
words_and_punct = []
words = ''
letter = ''
ex_sign = ''
list_of_words = []
exceptions_letters = []
numbers = []
token = []
spaces = ''
sentence = []

for i in sys.stdin.readlines():
    sentence.append(i)

for i in range(len(sentence)):
    print("# sent_id = %s" % i)
    print("# text = %s" % sentence[i])
#
    exception = re.findall('\w+\.\w+\.', sentence[i]) 
    three_stops = re.findall("\.\.\.", sentence[i]) 
    number = re.findall('\d+\.|\d+\)', sentence[i]) 
    thousands = re.findall('\d+\s\d+\s*\d*\s*\d*|\d+\s', sentence[i]) 
    hyphen = re.findall('\w+\-\w+', sentence[i]) 

    for b in exception: 
        for v in range(len(b)):
            if b[v].isalpha():
                letter += b[v]
                exceptions_letters.append(b[v])
                letter = ''
            if b[v] in punct:
                ex_sign += b[v]
                exceptions_letters.append(b[v])
                letter = ''

    reg = re.compile('\w+\.\w+\.')
    new_text = reg.sub('', sentence[i])
    reg = re.compile("\.\.\.")
    again_text = reg.sub('', new_text)
    reg = re.compile('\d+\.?|\d+\)?')
    a_new_text = reg.sub('', again_text)
    reg = re.compile('\w+\-\w+')
    a_new_one = reg.sub('', a_new_text)
    reg = re.compile('\d+\s\d+')
    text = reg.sub('', a_new_one)
   

    for i in range(len(text)): 

        if text[i].isalpha():
            words += text[i]
        if text[i] in punct:
            if text[i] == '„': 
                sign += text[i] + '“'
                list_of_sign.append(sign)
                sign = ''
            if text[i] == '(':
                sign += text[i] + ')'
                list_of_sign.append(sign)
                sign = ''
            else:
                sign += text[i]
                list_of_sign.append(sign)
                sign = ''
        if text[i] == ' ' or text[i] in punct:
            list_of_words.append(words)
            words = ''

    final_list_of_sign = [] 
    quote = int(list_of_sign.count('"'))
    for i in list_of_sign:
        if i != '"':
            final_list_of_sign.append(i)
    for i in range(int(quote/2)):
        final_list_of_sign.append('""')
    final_list_of_sign.extend(three_stops)

    token.extend(list_of_words)
    token.extend(exceptions_letters)
    token.extend(number)
    token.extend(thousands)
    token.extend(hyphen)
    token.extend(final_list_of_sign)
    token.extend(ex_sign)

tr_word = ''
f = open('transl.txt', 'r')
transliteration_vocab = f.readlines()
#print(type(transliteration_vocab))

#print(transliteration_vocab)
transliteration = {}

for i in transliteration_vocab:
    a = i.replace('\t', '')
    print(a)
    b = a.replace('\n', '')
    print(b)
    transliteration[a[0]] = b[1:]

print(transliteration)
    
#for i in transliteratin_vocab: 
    
for my_word in range(len(token)):
    for cz in range(len(my_word)): 
        if my_word[cz] in transliteration:
            tr_word += transliteration[my_word[cz]]
        else: 
            tr_word += my_word[cz]
    for k in token:

        if k != '' and k != '\n' and k != '„':
            m = re.sub(r'\s', '', k)
            len_t = len(k)
            space = 15 - len_t
            spaces = ''
            for i in range(space):
                spaces += ' '

print(m + spaces + "—" + "            " + "—" + "            " + "—" + "            " + "            " + "—" + "Translit=" + tr_word)       

print(tr_word)


