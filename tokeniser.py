import re
import sys

#here is the twist in the POS tagger. I found this one http://rdrpostagger.sourceforge.net/#_Toc435576451 (founded by chance) and decided that I can use it. So I have tagged and I edited its tags so I can do my own tagging. The tags are in 'my_text.txt'. Then I made a dictionary which has a word of the corpus as a key and its postag as a value. Then I compare my tokens with these keys

with open('my_text.txt', 'r', encoding='utf-8') as file:
    tags = {}
    letter = ''
    punct = ['.', ',', '?', '!', '"', '„', '“', '„', '“', ':', "(", "—"]
    for u in file:
        space_text = u.split(' ')
        for i in space_text:
            tag_text = i.split("/")
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
                    tag_text[1] = "PREP"
                elif tag_text[1][0] == "J":
                    tag_text[1] = "CONJ"
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
    #print("# sent_id = %s" % i)
    #print("# text = %s" % i)
    sentence.append(i)

for i in range(len(sentence)):
    print("# sent_id = %s" % i)
    print("# text = %s" % sentence[i])
#
    exception = re.findall('\w+\.\w+\.', sentence[i]) #search for pattern letter(s)-stop-letter(s)
    three_stops = re.findall("\.\.\.", sentence[i]) #search for ...
    number = re.findall('\d+\.|\d+\)', sentence[i]) #search for list numbering (1. or 1))
    thousands = re.findall('\d+\s\d+\s*\d*\s*\d*|\d+\s', sentence[i]) #search for numbers with space 4 5656 or numbers
    hyphen = re.findall('\w+\-\w+', sentence[i]) #search for -

    for b in exception: #here we form the list
        for v in range(len(b)):
            if b[v].isalpha():
                letter += b[v]
                exceptions_letters.append(b[v])
                letter = ''
            if b[v] in punct:
                ex_sign += b[v]
                exceptions_letters.append(b[v])
                letter = ''

    #the following part finds all the previous patterns in our line and then replace them with spaces
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
    #the end of this part

    for i in range(len(text)): #we want to form the list of words and the list of punctuation

        if text[i].isalpha():
            words += text[i]
        if text[i] in punct:
            if text[i] == '„': #i think that in the line „fggsyhsr“ these signs „“ should be tokenize as one. the same is for (). so () is one token
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

    final_list_of_sign = [] #that was described (() - as one token) can be used for "". but i have no idea how to do it better. so i count quotes, then replace the half of them with "" and never mind the second half
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

    for k in token:

        if k != '' and k != '\n' and k != '„':
            m = re.sub(r'\s', '', k)

            len_t = len(k)
            space = 15 - len_t
            spaces = ''
            for i in range(space):
                spaces += ' '

            print(m + spaces + "—" + "            " + "—" + "            " + "—" + "            " + tags.get(m, 'x')+ "            " + "—" + "            " + "—" + "            " + "—" + "            " + "—" + "            " + "—" )

        final_list_of_sign = []
        ex_sign = []
        three_stops = []
        numbers = []
        number = []
        thousands = []
        hyphen = []
        #exception = []
        sign = ''
        spaces = ''
        list_of_sign = []
        words_and_punct = []
        words = ''
        letter = ''
        ex_sign = ''
        list_of_words = []
        exceptions_letters = []
        exceptions_sign = []
        exceptions_letters = []
        numbers = []
        token = []

