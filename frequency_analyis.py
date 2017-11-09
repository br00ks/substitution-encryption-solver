import operator, re

# returns list with all n letter words from input
def get_n_letter_words(n, input, blank):
    n_list = []
    input = input.split(blank)
    for i in range(len(input) -n+1):
        current_word = input[i:i+1]
        if (len(current_word[0]) == n):
            n_list.append(input[i:i+1])

    return n_list

# returns list with all words from input matching given pattern
def find_pattern(pattern, cipher_key, input, blank):
    pattern_list = []
    input = input.split(blank)
    for word in input:
        m = re.search(pattern, word)
        print("---> current word: ")
        if (m):
            print(m.group(0))
    return pattern_list

# returns a list with occurring digraphs in input with frequency
def analyse_digraphs(input, blank):
    digraphs = []
    frequency = {}
    input = input.split(blank)
    for word in input:
        if (len(word) > 1):
            for i in range(len(word)):
                if(len(word[i:i+2]) == 2):
                    digraphs.append(word[i:i+2])

    for digraph in digraphs:
        frequency[digraph] = digraphs.count(digraph)

    return frequency

# returns a list with all occurring double letters in input words
def find_double_letters(input, blank):
    double_letters = []
    frequency = {}
    input = input.split(blank)
    regex = re.compile(r"(.)\1")
    for word in input:
        match = re.search(regex, word)
        if (match):
            double_letters.append(match.group(0))

    return double_letters

# Letter Frequency of the Most Common 1st Letter in Words
# http://letterfrequency.org/
# t o a w b c d s f m r h i y e g l n p u j k
# returns sorted list of tuples containing frequency of letters being first letters of a word
def count_first_letters(input, blank):
    occ = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0, 'k': 0,
                 'l': 0, 'm': 0, 'n': 0, 'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0, 'v': 0,
                 'w': 0, 'x': 0, 'y': 0, 'z': 0}

    temp = input.split(blank)
    for i in range(len(temp)):
        occ[temp[i][0]] = occ.get(temp[i][0]) + 1

    sorted_list = sorted(occ.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_list
