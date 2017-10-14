import sys 
import re

result = re.search(r'Analytics', 'AV Analytics Vidhya AV')
a = result.group(0)

#print(a)


sentences = []
tags_and_words = {}
filename = sys.argv[1]
text = open(filename, 'r')
for i in text.readlines(): 
    if "#" in i or "-" in i:
        continue
    else: 
        key_pattern = re.search(r'\t\w+\n|\t\:\n|\t\.+\n|\t\,\n|\t\(\)\n|\t\?\n|\t\!\n|\t\%\n|\t\—\n|\t\„\“\n|\t\"\"|\t\w+$', i)
        if key_pattern:

            key = key_pattern.group(0)
            print(key)
        value_pattern = re.search(r'\t\D+\t', i)
        if value_pattern:
            value = value_pattern.group(0)
        tags_and_words[key[1:len(key)-1]] = value[1:len(value)-1]

#print(len(tags_and_words))
    
#print(tags_and_words)

for i in sys.stdin.readlines():	
    #print(i)
    if i[0] =='#':
        print(i)
    else:   
        #print(' - ', i)

        word_pattern = re.match('\w+|\:|\,|\.+|\!|\?|\(\)|\"\"|\%|\—|\„\“', i) 
        if word_pattern:
            #print(word_pattern)
            word = word_pattern.group(0)
            print(word + "\t" + "—" + "\t" + "—" + "\t" + "—" + "\t" + "\t" + "—" + "\t" + tags_and_words[word] + " \t" + "—" + "\t" + "—" + "\t" + "—" )
