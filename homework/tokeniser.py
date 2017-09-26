# -*- coding: utf-8 -*-

#this is madness
import re
plain_text = sys.stdin.read()

punct = ['.', ',', '?', '!', '"', '„', '“', '„', '“', ':', "(", "—", "%"]
sign = ''
list_of_sign = []
words_and_punct = []
words = ''
letter = ''
ex_sign = ''
list_of_words = []
exceptions_letters = []
exceptions_sign = []
numbers = []
token = []

exception = re.findall('\w+\.\w+\.', plain_text) #search for pattern letter(s)-stop-letter(s)
three_stops = re.findall("\.\.\.", plain_text) #search for ...
number = re.findall('\d+\.?|\d+\)?', plain_text) #search for numbers wittout space (2344 or 12 or 344356) and for list numbering (1. or 1)
thousands = re.findall('\d+\s\d+', plain_text) #search for numbers with space 4 5656
hyphen = re.findall('\w+\-\w+', plain_text) #search for -

for b in exception: #here we form two lists. exception_letters has letters from the patters letter(s)-stop-letter(s), exception_sign has signs
    for v in range(len(b)):
        if b[v].isalpha():
            letter += b[v]
            exceptions_letters.append(b[v])
            letter = ''
        if b[v] in punct:
            ex_sign += b[v]
            exceptions_sign.append(b[v])
            ex_sign = ''

#the following part finds all the previous patterns in our line and then replace them with spaces
reg = re.compile('\w+\.\w+\.')
new_text = reg.sub('', plain_text)
reg = re.compile("\.\.\.")
again_text = reg.sub("", new_text)
reg = re.compile('\d+\.?|\d+\)?')
a_new_text = reg.sub('', again_text)
reg = re.compile('\w+\-\w+')
a_new_one = reg.sub('', a_new_text)
reg = re.compile('\d+\s\d+')
text = reg.sub('', a_new_one)
#the end of this part

for i in range(len(text)): #we want to form the list of words and the list of punctuation
    if text[i].isalpha():
        words += text[i]
    if text[i] in punct:
        if text[i] == '„': #i think that in the line „fggsyhsr“ these signs „ “ should be tokenize as one. the same is for (). so () - this is one token
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
    if text[i] == ' ':
        list_of_words.append(words)
        words = ''

final_list_of_sign = [] #that was described (() - as one token) can be used for "". but i have no idea how to do it better. so i count quotes, then replace the half of them with "" and never mind the second half
quote = int(list_of_sign.count('"'))
for i in list_of_sign:
    if i != '"':
        final_list_of_sign.append(i)
for i in range(int(quote/2)):
    final_list_of_sign.append('""')
final_list_of_sign.extend(three_stops)

token.extend(final_list_of_sign)
token.extend(ex_sign)
token.extend(three_stops)
token.extend(number)
token.extend(thousands)
token.extend(hyphen)
token.extend(list_of_words)

for i in token:
    if i != '':
        print(i)
