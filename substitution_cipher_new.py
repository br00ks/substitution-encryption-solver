import enchant, operator, frequency_analyis, re

letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
abc = "abcdefghijklmnopqrstuvwxyz"
file = open("C:/Users/Karin/PycharmProjects/ue1_svs/sample_encrypted.txt", "r").read().lower()
#file = "Rboerpktigoevcrbebwucjaewjeklojehcjd,ekm sktpqo,ecqerbwreloklgoevcggecjqcqrekjeskhcjaewgkjaewjderpycjaerkeltrerbcjaqecjecr".lower()
dictionary = enchant.Dict("en_US")
letter_occurrence = {}
cipher_key = {'a': [], 'b': [], 'c': [], 'd': [], 'e': [], 'f': [], 'g': [], 'h': [], 'i': [], 'j': [], 'k': [], 'l': [], 'm': [], 'n': [], 'o': [], 'p': [], 'q': [], 'r': [], 's': [], 't': [], 'u': [], 'v': [], 'w': [], 'x': [], 'y': [], 'z': []}
letter_frequencies = {'a': [], 'b': [], 'c': [], 'd': [], 'e': [], 'f': [], 'g': [], 'h': [], 'i': [], 'j': [], 'k': [], 'l': [], 'm': [], 'n': [], 'o': [], 'p': [], 'q': [], 'r': [], 's': [], 't': [], 'u': [], 'v': [], 'w': [], 'x': [], 'y': [], 'z': []}
letter_candidates = {'a': [], 'b': [], 'c': [], 'd': [], 'e': [], 'f': [], 'g': [], 'h': [], 'i': [], 'j': [], 'k': [], 'l': [], 'm': [], 'n': [], 'o': [], 'p': [], 'q': [], 'r': [], 's': [], 't': [], 'u': [], 'v': [], 'w': [], 'x': [], 'y': [], 'z': []}
# letter frequency taken from : https://inventwithpython.com/hacking/chapter20.html
english_letter_frequency = {'e': 12.70, 't': 9.06, 'a': 8.17, 'o': 7.51, 'i': 6.97, 'n': 6.75, 's': 6.33, 'h': 6.09, 'r': 5.99, 'd': 4.25, 'l': 4.03, 'c': 2.78, 'u': 2.76, 'm': 2.41, 'w': 2.36, 'f': 2.23, 'g': 2.02, 'y': 1.97, 'p': 1.93, 'b': 1.29, 'v': 0.98, 'k': 0.77, 'j': 0.15, 'x': 0.15, 'q': 0.10, 'z': 0.07}

# frequencies taken from : https://www3.nd.edu/~busiforc/handouts/cryptography/cryptography%20hints.html
# https://www3.nd.edu/~busiforc/handouts/cryptography/cryptography%20hints.html
two_letters = ['of', 'to', 'in', 'it', 'is', 'be', 'as', 'at', 'so', 'we', 'he', 'by', 'or', 'on', 'do', 'if', 'me', 'my', 'up', 'an', 'go', 'no', 'us', 'am']
three_letters = ['the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'any', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use']
four_letters = ['that', 'with', 'have', 'this', 'will', 'your', 'from', 'they', 'know', 'want', 'been', 'good', 'much', 'some', 'time']# method to find blank

# we assume that most frequent letter is encrypted blank
def find_blank():
    last = ''
    before_last = ''
    maybe_blank = []
    maybe_a_or_i_patterns = []

    for character in file:
        if (before_last == character and last != character):
            pattern = before_last + last + character
            # print("here we go... !!!")
            maybe_blank.append(character)
            maybe_a_or_i_patterns.append(pattern)

        before_last = last
        last = character

    most_frequent_letter = ''
    for letter in maybe_blank:
        if (most_frequent_letter):
            if (maybe_blank.count(letter) > maybe_blank.count(most_frequent_letter)):
                most_frequent_letter = letter
        else:
            most_frequent_letter = letter

    cipher_key[most_frequent_letter] = ' '
    # blank_letter = mostFrequentLetter

    print("now we know that our blank is: "+most_frequent_letter)

    temp = []
    frequency_temp = {}
    for pattern in maybe_a_or_i_patterns:
        regex = most_frequent_letter + r'.' + most_frequent_letter
        match = re.match(regex, pattern)
        if (match):
            string = match.group(0)
            curr_letter = string.replace(most_frequent_letter, "")
            if (curr_letter not in temp):
                temp.append(string.replace(most_frequent_letter, ""))

    for candidate in temp:
        frequency_temp[candidate] = file.count(candidate)/len(file)
        # set to remember
        letter_candidates[candidate] += 'a'
        letter_candidates[candidate] += 'i'

    # we now that "a" is more frequent in english texts than "i" so we are going to set the more frequent
    # letter to be the "a" letter
    frequency_temp_sorted = sorted(frequency_temp.items(), key=operator.itemgetter(1), reverse=True)
    print(frequency_temp_sorted)
    from operator import itemgetter
    mostFrequent = itemgetter(1)(frequency_temp_sorted)[0]
    secondMostFrequent = itemgetter(-2)(frequency_temp_sorted)[0]
    cipher_key[mostFrequent] = 'a'
    cipher_key[secondMostFrequent] = 'i'

# function that returns the letter which is defined as blank
def get_blank():
    for key, value in cipher_key.items():
        if value == ' ':
            return key
    return ' '

def count_letters():
    file_length = len(file)

    for i in letters:
        occ = file.count(i)
        letter_occurrence[i] = occ
        letter_frequencies[i] = (occ/file_length)*100

    sorted_dict = sorted(letter_frequencies.items(), key=operator.itemgetter(1), reverse=True)
    print(sorted_dict)
    from operator import itemgetter
    mostFrequent = itemgetter(1)(sorted_dict)[0]
    secondMostFrequent = itemgetter(2)(sorted_dict)[0]

    # most frequent letter is e
    if (cipher_key[mostFrequent] != ''):
        cipher_key[secondMostFrequent] = 'e'
    else:
        cipher_key[mostFrequent] = 'e'

#def etaion():

def analyse_bigrams():
    twoletterwords = frequency_analyis.get_n_letter_words(2, file, get_blank())
    occ = {}
    print(twoletterwords)
    # most common two letter word is "of" followed by to, in, it...
    for word in twoletterwords:
        occ[word[0]] = twoletterwords.count(word)

    sorted_list = sorted(occ.items(), key=operator.itemgetter(1), reverse=True)
    print(sorted_list)

    if (sorted_list):
        mostFrequent = sorted_list[0][0]
        letter_candidates[mostFrequent[0]] = 'o'
        letter_candidates[mostFrequent[1]] = 'f'

def analyse_trigrams():
    threeletterwords = frequency_analyis.get_n_letter_words(3, file, get_blank())
    occ = {}
    # most common three letter word is "the", followed by "and", "for" ,..
    for word in threeletterwords:
        occ[word[0]] = threeletterwords.count(word)

    sorted_list = sorted(occ.items(), key=operator.itemgetter(1), reverse=True)
    print(sorted_list)
    print("three letter words: ")
    mostFrequent = sorted_list[0][0] # supposed to be "the"
    secondMostFrequent = sorted_list[1][0] # supposed to be "and"

    # was hab ich mir dabei gedacht????? warum diese if-anweisung?
    if (mostFrequent[0]):
        cipher_key[mostFrequent[0]] = 't'
    else:
        letter_candidates[mostFrequent[0]] += 't'

    if (mostFrequent[1]):
        cipher_key[mostFrequent[1]] = 'h'
    else:
        letter_candidates[mostFrequent[1]] += 'h'

    if (mostFrequent[2]):
        cipher_key[mostFrequent[2]] = 'e'
    else:
        letter_candidates[mostFrequent[2]] += 'e'

    if (secondMostFrequent[0]):
        cipher_key[secondMostFrequent[0]] = 'a'
        # and now that we know which letter is a:
        # we can set I:
        for key, value in letter_candidates.items():
            if('i' in value and key != secondMostFrequent[0]):
                # set cipher key to be this values
                cipher_key[key] = 'i'

    else:
        letter_candidates[secondMostFrequent[0]] += 'a'

    if (secondMostFrequent[1]):
        cipher_key[secondMostFrequent[1]] = 'n'
    else:
        letter_candidates[secondMostFrequent[1]] += 'n'

    if (secondMostFrequent[2]):
        cipher_key[secondMostFrequent[2]] = 'd'
    else:
        letter_candidates[secondMostFrequent[2]] += 'd'

    # the and and are set, now we can try to find "are"
    #for word in threeletterwords:
        #if([word[0][0]

# .... all appearing only 1 time... so we can't tell anything from frequency....
def analyse_quadrigams():
    print("analysing quadrigams:")
    fourletterwords = frequency_analyis.get_n_letter_words(4, file, get_blank())
    occ = {}
    print(fourletterwords)
    for word in fourletterwords:
        occ[word[0]] = fourletterwords.count(word)
        if(word[0][0] == word[0][3]):
            print(word)
            print("this word must be THAT")

        if(word[0][2] == word[0][3]):
            print(word)
            print("this word must be WILL")
            string = 'will'
            i = 0
            while (i < 4):
                set_letter(word[0][i], string[i])
                i = i + 1


def set_letter(encrypted_letter, original_letter):
    cipher_key[encrypted_letter] = original_letter

def get_key_by_value(val_to_be_found, dict):
    for key, value in dict.items():
        if (value == val_to_be_found):
            return key

def analyse_patterns():
    # most common patterns: t followed by h, e followed by r
    # two letter words: "to"
    digraph_frequency = frequency_analyis.analyse_digraphs(file, get_blank())
    sorted_frequency_digraphs = sorted(digraph_frequency.items(), key=operator.itemgetter(1), reverse=True)
    print("sorted frequency digraphs: ")
    print(sorted_frequency_digraphs)
    print("at this point we already know letters for 'the'")

    # find double letters
    double_letters = frequency_analyis.find_double_letters(file, get_blank())
    frequency = {}
    print(double_letters)

    for double in double_letters:
        print(double)
        if (frequency.get(str(double))):
            frequency[str(double)] += 1
        else:
            frequency[str(double)] = 1

    # check: letzte drei buchstaben, wenn in*, dann ing...?
    words = file.split(get_blank())
    if (get_key_by_value('i', cipher_key) and get_key_by_value('n', cipher_key)):
        i = get_key_by_value('i', cipher_key)
        n = get_key_by_value('n', cipher_key)
        matches = []
        for word in words:
            m = re.search(i+n+'.', word) # search pattern in + anything
            if(m):
                matches.append(m.group(0))

        matches_counted = {}
        for match in matches:
            occ = matches.count(match)
            matches_counted[match] = occ

        print(matches_counted)
        matches_sorted = sorted(matches_counted.items(), key=operator.itemgetter(1), reverse=True)
        from operator import itemgetter
        ing = itemgetter(0)(matches_sorted)[0]
        print(ing[2])
        cipher_key[ing[2]] = 'g'

def output_word(word):
    output = ""
    for character in word:
        if (cipher_key.get(character) or letter_candidates.get(character)):
            if (cipher_key.get(character)):
                output += cipher_key.get(character)
            else:
                output += str(letter_candidates.get(character))
        else:
            output += '*'
    return output

# checks the current input and counts how many of the decrypted words exist
def check_word(word, counter, original_text, score):
    global cipher_key
    word = output_word(word)
    if (dictionary.check(word)):
        return
    else:
        #if (len(word) >= 4 and word.count("*") <= 2):
        if (word.count("*") * 2 < len(word)):
            if (dictionary.suggest(word)):
                # print(word)
                # print(original_text[counter])
                suggestions = dictionary.suggest(word)
                # now check every suggested word, when we set the new letter, if it
                # improves the score
                for suggestedword in suggestions[:3]:
                    #print(word)
                    current_word = suggestedword.lower();
                    if (len(current_word) == len(word)):
                        # print(current_letter)
                        indices = get_indices(word)
                        #print(word)
                        #print(indices)
                        cipher_key_copy = cipher_key
                        for index in indices:
                            letter_to_decrypt = current_word[index]
                            print(current_word)
                            print("letter to decrpy: ")
                            print(letter_to_decrypt)
                            if (letter_to_decrypt in cipher_key.values()):
                                print("already set...")
                                set = get_key_by_value(letter_to_decrypt, cipher_key)
                                print(set)
                                current_orig_word = original_text[counter]
                                original_value = cipher_key.get(set)
                                print("original: ")
                                print(original_value)
                                cipher_key[current_orig_word[index]] = letter_to_decrypt
                                cipher_key[set] = ''
                                new_score = check_score()
                                if (new_score <= score):
                                    cipher_key[current_orig_word[index]] = ''
                                    cipher_key[set] = original_value
                                    continue
                                else:
                                    return
                            else:
                                current_orig_word = original_text[counter]
                                original_value = cipher_key[current_orig_word[index]]
                                cipher_key[current_orig_word[index]] = letter_to_decrypt
                                print(output())
                                print(cipher_key)

                        new_score = check_score()
                        print("NEW SCORE: ")
                        print(new_score)
                        print(cipher_key)
                        if (new_score <= score):
                            cipher_key = cipher_key_copy
                            continue
                        else:
                            return

def get_indices(decrypted):
    indices = []
    counter = 0
    for char in decrypted:
        if(char == "*"):
            indices.append(counter)
            counter = 0
        counter += 1
    return indices

def check_score():
    score = 0
    decrypted_text = output()
    decrypted_text = decrypted_text.split(" ")
    print(decrypted_text)
    for word in decrypted_text:
        if (dictionary.check(word)):
            score += 1
    return score
    #if (dictionary.suggest(input)):
    #    print(dictionary.suggest(input))

# here we start analysing the text
# out text is already split and we have two possible candidates for "a" and "i"
def start_analysing():
    # the most common first letter in words is "t" followed by "o" "a" "w" "b"
    frequency_list = frequency_analyis.count_first_letters(file,get_blank())
    print(frequency_list)
    cipher_key[frequency_list[0][0]] = 't'
    analyse_bigrams()
    analyse_trigrams()
    analyse_quadrigams()
    analyse_patterns()
    start_decrypting()

def analyse_words():
    # try to find out words where only length of word minus 1 or minus 2 when length > 6 letters missing
    print("analysing")
    # here : get words, split on blank, find words where only ... missing... try to find out with enchant

def start_decrypting():
    print("START DECRYPTING")
    score = check_score();
    original_text = file.split(get_blank());
    words_len = len(original_text)

    # as long as not all words are recognized as existing words
    counter = 0
    for word in original_text:
        if (score != words_len):
            check_word(word, counter, original_text, score)
            score = check_score()
            counter += 1

def output():
    output = ""
    for character in file:
        if(cipher_key.get(character) or letter_candidates.get(character)):
            if(cipher_key.get(character)):
                output += cipher_key.get(character)
            else:
                output += str(letter_candidates.get(character))
        else:
            output += '*'
    return output

def decrypt(file, dictionary):

    if (len(file.split(" ")) <=  1):
        print("blank is also ciphered")
        find_blank()

    count_letters()
    start_analysing()
    start_decrypting()
    print(frequency_analyis.get_n_letter_words(2, file, get_blank()))
    print(output())
    # print(cipher_key)

def main():
    decrypt(file, dictionary)

main()