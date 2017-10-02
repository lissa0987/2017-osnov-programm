import sys
text = sys.stdin.read()

text.translate('\n')
punc = ['.', '?', '!']
sentence = []
sentence_start = 0
sentence_end = 0
for i in range(len(text)-2):
    
    if text[i] in punc and text[i + 1] == ' ' and text[i-2].isalnum():#check the end of the sentence
        sentence_end = i + 1
        sentence.append(text[sentence_start:sentence_end])
        sentence_start = sentence_end + 1
    if text[i] in punc and text[i + 1].isalnum and text[i-2].isalnum():#check the end of the sentence
        sentence_end = i 
        sentence.append(text[sentence_start:sentence_end])
        sentence_start = sentence_end + 1

    if (text[i] == '"' or text[i] == '»') and text[i-1] in punc and text[i-2].isalnum(): #exeptions
        m = text[i]
        sentence_end = i + 1
        sentence.append(text[sentence_start:sentence_end])
        sentence_start = sentence_end + 1

sentence.append(text[sentence_start:len(text)])
for i in sentence:
    sys.stdout.write(i)
