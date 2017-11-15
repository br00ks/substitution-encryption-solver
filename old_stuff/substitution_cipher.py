import enchant
import operator
import re

letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
cipher_key = {'a': [], 'b': [], 'c': [], 'd': [], 'e': [], 'f': [], 'g': [], 'h': [], 'i': [], 'j': [], 'k': [], 'l': [], 'm': [], 'n': [], 'o': [], 'p': [], 'q': [], 'r': [], 's': [], 't': [], 'u': [], 'v': [], 'w': [], 'x': [], 'y': [], 'z': []}
file = open("C:/Users/Karin/PycharmProjects/ue1_svs/sample_encrypted.txt", "r").read().lower()
dictionary = enchant.Dict("en_US")
blank = ''
sorted_dict = {}
letter_occurrence = {}

# we can assume that a letter surrounded by the same letters could be A or I
# the letters around that letter must be the letter for "blank"
def find_blank():
    last = ''
    before_last = ''
    maybe_blank = []
    maybe_a_or_i = []

    for character in file:
        if (before_last == character and last != character):
            #print(character)
           # print("here we go... !!!")
            maybe_a_or_i.append(last)
            maybe_blank.append(character)

        before_last = last
        last = character

    print(maybe_blank)
    print(maybe_a_or_i)

    mostFrequentLetter = ''
    for letter in maybe_blank:
        if (mostFrequentLetter != ''):
            if (maybe_blank.count(letter) > maybe_blank.count(mostFrequentLetter)):
                mostFrequentLetter = letter
        else:
            mostFrequentLetter = letter

    cipher_key[mostFrequentLetter] = ' '
    blank = mostFrequentLetter

def count_letters():

    for i in letters:
        letter_occurrence[i] = file.count(i)

    # most frequent letter is usually 'e'
    # print(sorted(letter_occurrence.values()))

    # returns a sorted list of tuples
    sorted_dict = sorted(letter_occurrence.items(), key=operator.itemgetter(1))
    print(sorted_dict)

    # get last tuple from sorted list and set "e" in cipherkey to most common letter
    from operator import itemgetter
    mostFrequent = itemgetter(-1)(sorted_dict)[0]
    secondMostFrequent = itemgetter(-2)(sorted_dict)[0]
    thirdMostFrequent = itemgetter(-3)(sorted_dict)[0]
    cipher_key[mostFrequent] = 'e'
    cipher_key[secondMostFrequent] = 't'
    cipher_key[thirdMostFrequent] = 'a'

    # get least frequent characters... but not working very well... :(
    # least frequent and second least frequent could be the same (in this case: 0 )
    # which one to choose for y,z??

    leastFrequent = itemgetter(0)(sorted_dict)[0]
    secondLeastFrequent = itemgetter(1)(sorted_dict)[0]

# set random key for all values that haven't been set
def set_random_key():
    characters = "etaoinshrdlcumwfgypbvkjxqz" # sorted by frequency
    for key in cipher_key.keys():
        if cipher_key[key]:
            characters = characters.replace(cipher_key[key], "")

    print("remaining characters: "+ characters)

    for key in sorted(letter_occurrence.items(), key=operator.itemgetter(1)):
        print(key[0])
        #array = list(characters)
        #length = len(array) - 1
        #print(array[length])
        #cipher_key[key[0]] = array[length]
        #characters = characters.replace(key[0], "")
        #print("characters now: "+characters)
        #print("key "+key[0]+", value: "+str(letter_occurrence[key[0]]))
    print(cipher_key)

def decrypt(text, dictionary):
    find_blank()
    count_letters()
    set_random_key()
    print(dictionary.check("Hello"))

def main():
    decrypt(file, dictionary)
    print(cipher_key)

main()