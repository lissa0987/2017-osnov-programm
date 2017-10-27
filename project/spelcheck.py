import re
import sys


#we have two parts of the programm. The first one counts edit distance (the idea was found https://habrahabr.ru/post/117063/ and http://www.let.rug.nl/~kleiweg/lev/). The second one does the checking. The input is txt file with the text that should be edited. The output looks like word - its correction - edit distance. The programm shoud be run python3 spelcheck.py the name of the reference corpus the name of the text. Brown corpus was taken as a reference corpus 
def get_edit_distance(word1, word2):
    len_word1 = len(word1)
    len_word2 = len(word2)
    accum = {}
    def _d(i,j):#i, j - possitions in the word
        rt = 0
        zn = accum.get((i,j), 0)#check if the know the difference, if we have nothing it returns 0

        if zn != 0:#if we have something - we find the distance for these letters
            rt = zn
        elif i < 0 and j < 0:#out of range
            rt = 0
        elif i < 0:#we insert or delet the symbol
            rt = j + 1
        elif j < 0:
            rt = i + 1
        else:
            rt1 = _d(i-1, j) + 1#what if we delete the symbol
            rt2 = _d(i, j-1) + 1#what if we add the symbol
            if word1[i] != word2[j]:#what if we replace the symbol
                rt3 = _d(i-1, j-1) + 1
            else:
                rt3 = _d(i-1, j-1) + 0
            rt = min(rt1,rt2, rt3)
            accum[i,j] = rt
        return rt
    for i in range(len_word1):
        for j in range(len_word2):
            _d(i,j)
    result = _d(len_word1-1, len_word2-1)
    #print(result)
    return result

#print(get_edit_distance('point', 'sirloin '))

def get_words():# tokenization of the corpus. ignore the punctuation as it does not matter
    corpus = sys.argv[1]
    with open(corpus, 'r') as f:
        a = f.read()
        corpus_tokens = re.findall('\w+', a)
    return corpus_tokens


# get_words('brown.txt')

def det_counts(corpus_tokens):  # frequecy vocab: {token:frequency}; frequency is how often the word appears in the corpus
    frequency_vocab = {}
    for a in corpus_tokens:
        frequency_vocab[a] = frequency_vocab.setdefault(a, 0) + 1  # returns the value and add 1
    return frequency_vocab


def get_text():  # tokenization of the text. ignore the punctuation as it does not matter
    text = sys.argv[2]
    with open(text, 'r') as f:
        a = f.read()
        text_tokens = re.findall('\w+', a)
    return text_tokens


def get_edits1():  # how we can trasform the word (where we can make a mistake)
    # n = w
    transformed_word = ''
    list_of_transformations = []
    transfrom_vocab = {}
    words_from_text = get_text()
    for word in words_from_text:
        for i in range(len(word)):  # one letter is missing
            second_part = word[i + 1:]
            first_part = word[:i]
            list_of_transformations.append(first_part + second_part)
        print(list_of_transformations)
        transfrom_vocab[word] = list_of_transformations
        list_of_transformations = []
        for i in range(len(word) - 1):  # two letters replace each other (cat - cta...)
            second_part = word[i + 2:]
            first_part = word[:i]
            list_of_transformations.append(first_part + word[i + 1] + word[i] + second_part)
        print(list_of_transformations)
        transfrom_vocab[word] = list_of_transformations
        list_of_transformations = []
        alph = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x',
                'v', 'c', 'b', 'n', 'm']
        for i in range(len(word)):  # a letter is replaced by any letter
            second_part = word[i + 1:]
            first_part = word[:i]
            for q in range(len(alph)):
                list_of_transformations.append(first_part + alph[q] + second_part)
        print(list_of_transformations)
        transfrom_vocab[word] = list_of_transformations
        list_of_transformations = []
        for i in range(len(word) + 1):  # a letter is inserted somewhere in the word
            g = word[i:]
            h = word[:i]
            for e in range(len(alph)):
                list_of_transformations.append(h + alph[e] + g)
        print(list_of_transformations)
        transfrom_vocab[word] = list_of_transformations
        list_of_transformations = []
    return transfrom_vocab


def get_most_likely():  # spellchecking
    vocab = det_counts(get_words())  # form our vocab
    transformation = get_edits1()  # change the word
    #print(transformation)
    word = get_text()#words in text
    corrections = []
    #words_transformation = []


# words = l
    amount = 0
    freq_word = ""
    final_word = ''

    for i in word:
        amount = 0
        freq_word = ""
        final_word = ''
        words_transformation = transformation.get(i)
        for m in words_transformation:  # find the most frequent word
            if amount < vocab.get(m, 0):
                amount = vocab[m]
                freq_word = m

        if vocab.get(i, 0) > 0:#if the word is in the frequency vocab
            final_word = i
            distance = get_edit_distance(i, final_word)
            print(i + '\t\t' + final_word + '\t\t' + str(distance))
            corrections.append(final_word)
        else:
            if vocab.get(freq_word, 0) != 0:  # find the transformation
                final_word = freq_word
                distance = get_edit_distance(i, final_word)
                print(i + '\t\t' + final_word + '\t\t'+ str(distance))
                corrections.append(final_word)
            else:  # no word (and its transformation) in the vocab
                print(i + "\t\t" +'no correction is found:( Try these:')
                words_in_the_ref_corp = get_words()
                #for q in words_transformation:
                variants = {}
                for w in words_in_the_ref_corp:
                    dist = get_edit_distance(i, w)
                    variants[dist] = w
                sorted_vocab = sorted(variants.keys())
                #print(sorted_vocab)
                for e in range(4):
                    possible_word = variants[sorted_vocab[e]]
                    print('\t\t' + possible_word + '\t\t' + str(sorted_vocab[e]))
                        

                    #if amount < vocab.get(q,0):
                     #   the_most_frequent
                
                #corrections.append(final_word)



    return corrections

print(get_most_likely())

