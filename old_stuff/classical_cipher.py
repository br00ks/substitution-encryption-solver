import operator
# http://www.richkni.co.uk/php/crypta/freq.php - frequency of letters in english texts
# idea simple substitution cipher (in theory):
# 1. find word pattern for each cipherword in cyphertext
# 2.

# only for english ASCII letters, texts with blanks!

letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
oneLetterWords = ['a', 'i']
# most frequent bigrams, trigrams..
# https://www3.nd.edu/~busiforc/handouts/cryptography/cryptography%20hints.html
twoLetterWords = ['of', 'to', 'in', 'it', 'is', 'be', 'as', 'at', 'so', 'we', 'he', 'by', 'or', 'on', 'do', 'if', 'me', 'my', 'up', 'an', 'go', 'no', 'us', 'am']
threeLetterWords = ['the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'any', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use']
fourLetterWords = ['that', 'with', 'have', 'this', 'will', 'your', 'from', 'they', 'know', 'want', 'been', 'good', 'much', 'some', 'time']

cipherKey = {'a': [], 'b': [], 'c': [], 'd': [], 'e': [], 'f': [], 'g': [], 'h': [], 'i': [], 'j': [], 'k': [], 'l': [], 'm': [], 'n': [], 'o': [], 'p': [], 'q': [], 'r': [], 's': [], 't': [], 'u': [], 'v': [], 'w': [], 'x': [], 'y': [], 'z': []}
file = open("C:/Users/Karin/PycharmProjects/ue1_svs/sample_encrypted.txt", "r").read().lower()

letterOccurence = {}

# first step: occurences , get most frequent letters, in english: e, t, (a, i, n, o s)
# thesis 1: most frequent letter --> 'e', second most frequent letter in text --> 't'

# second step:  letter pair frequencies, most frequent: th, he, in, er, an, re, nd, on, en, at
# https://www3.nd.edu/~busiforc/handouts/cryptography/Letter%20Frequencies.html#bigrams
# thesis 2:

# third step: trigams, most frequent: the, and, ing, her, hat, his, tha, ere, for, ent, ion...
# https://www3.nd.edu/~busiforc/handouts/cryptography/Letter%20Frequencies.html#bigrams
# thesis 3:

# forth step: quadrigrams, most frequent: that, ther, with, tion, here, ould, ight, have, hich, whic, this, thin, they
# https://www3.nd.edu/~busiforc/handouts/cryptography/Letter%20Frequencies.html#bigrams

def countLetters():

    for i in letters:
        letterOccurence[i] = file.count(i)

    # most frequent letter is usually 'e'
    # print(sorted(letterOccurence.values()))

    # returns a sorted list of tuples
    sortedDict = sorted(letterOccurence.items(), key=operator.itemgetter(1))
    print(sortedDict)

    # get last tuple from sorted list and set "e" in cipherkey to most common letter
    from operator import itemgetter
    mostFrequent = itemgetter(-1)(sortedDict)[0]
    secondMostFrequent = itemgetter(-2)(sortedDict)[0]
    thirdMostFrequent = itemgetter(-3)(sortedDict)[0]
    cipherKey[mostFrequent] = 'e'
    cipherKey[secondMostFrequent] = 't'
    cipherKey[thirdMostFrequent] = 'a'

    # get least frequent characters... but not working very well... :(
    # least frequent and second least frequent could be the same (in this case: 0 )
    # which one to choose for y,z??
    leastFrequent = itemgetter(0)(sortedDict)[0]
    secondLeastFrequent = itemgetter(1)(sortedDict)[0]

# we can assume that a letter surrounded by the same letters could be A or I
# the letters around that letter must be the letter for "blank"
def findBlank():
    last = ''
    beforeLast = ''
    maybeBlank = []
    maybeAorI = []

    for character in file:
        #print("current "+character)
        #print("last: "+last)
       # print("before last: "+beforeLast)

        if (beforeLast == character and last != character):
            #print(character)
           # print("here we go... !!!")
            maybeAorI.append(last)
            maybeBlank.append(character)

        beforeLast = last
        last = character

    print(maybeBlank)
    print(maybeAorI)

    mostFrequentLetter = ''
    for letter in maybeBlank:
        print(maybeBlank.count(letter))
        if (mostFrequentLetter != ''):
            if (maybeBlank.count(letter) > maybeBlank.count(mostFrequentLetter)):
                mostFrequentLetter = letter
        else:
            mostFrequentLetter = letter

    print("MOST FREQUENT LETTER: "+mostFrequentLetter)

    if (cipherKey[mostFrequentLetter] == ''):
        cipherKey[mostFrequentLetter] = ' '
    else:
        formerLetter = cipherKey[mostFrequentLetter]
        cipherKey[mostFrequentLetter] = ' '

    #for i in letters:
    #    blankOccurence['e'+i] = file.count('e'+i)

    #print(sorted(blankOccurence.values()))

    #for key, val in blankOccurence.items():
    #    print(key, " : ", val)

def check2letterWords():
    print("test")

def decrypt():
    output = ""
    for character in file:
        if(cipherKey.get(character)):
            output += cipherKey.get(character)
        else:
            output += '*'

    print(output)

def main():
    countLetters()
    print(letterOccurence)
    findBlank()
    check2letterWords()
    decrypt()
    print(cipherKey)
    print(file)

main()