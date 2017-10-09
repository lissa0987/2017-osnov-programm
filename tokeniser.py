import re
import sys

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

            print(m + spaces + "—" + "            " + "—" + "            " + "—" + "            " + "            " + "—" + "            " + "—" + "            " + "—" + "            " + "—" + "            " + "—" )

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

