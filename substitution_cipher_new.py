import enchant, operator, frequency_analyis, re

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z']
# abc = "abcdefghijklmnopqrstuvwxyz"
file = open("C:/Users/Karin/PycharmProjects/ue1_svs/svs/sample_encrypted.txt", "r").read().lower()
# file_original = open("C:/Users/Karin/PycharmProjects/ue1_svs/svs/sample_original", "r").read().lower()
# file = open("C:/Users/Karin/PycharmProjects/ue1_svs/svs/another_example.txt", "r").read().lower()
dictionary = enchant.Dict("en_US")
letter_occurrence = {}
cipher_key = {'a': [], 'b': [], 'c': [], 'd': [], 'e': [], 'f': [], 'g': [], 'h': [], 'i': [], 'j': [], 'k': [],
              'l': [], 'm': [], 'n': [], 'o': [], 'p': [], 'q': [], 'r': [], 's': [], 't': [], 'u': [], 'v': [],
              'w': [], 'x': [], 'y': [], 'z': []}
letter_frequencies = {'a': [], 'b': [], 'c': [], 'd': [], 'e': [], 'f': [], 'g': [], 'h': [], 'i': [], 'j': [], 'k': [],
                      'l': [], 'm': [], 'n': [], 'o': [], 'p': [], 'q': [], 'r': [], 's': [], 't': [], 'u': [], 'v': [],
                      'w': [], 'x': [], 'y': [], 'z': []}
letter_candidates = {'a': [], 'b': [], 'c': [], 'd': [], 'e': [], 'f': [], 'g': [], 'h': [], 'i': [], 'j': [], 'k': [],
                     'l': [], 'm': [], 'n': [], 'o': [], 'p': [], 'q': [], 'r': [], 's': [], 't': [], 'u': [], 'v': [],
                     'w': [], 'x': [], 'y': [], 'z': []}

# letter frequency taken from : https://inventwithpython.com/hacking/chapter20.html
# english_letter_frequency = {'e': 12.70, 't': 9.06, 'a': 8.17, 'o': 7.51, 'i': 6.97, 'n': 6.75, 's': 6.33, 'h': 6.09,
#                            'r': 5.99, 'd': 4.25, 'l': 4.03, 'c': 2.78, 'u': 2.76, 'm': 2.41, 'w': 2.36, 'f': 2.23,
#                            'g': 2.02, 'y': 1.97, 'p': 1.93, 'b': 1.29, 'v': 0.98, 'k': 0.77, 'j': 0.15, 'x': 0.15,
#                            'q': 0.10, 'z': 0.07}

# frequencies taken from : https://www3.nd.edu/~busiforc/handouts/cryptography/cryptography%20hints.html
# https://www3.nd.edu/~busiforc/handouts/cryptography/cryptography%20hints.html
# sorted by average occurrences
two_letters = ['of', 'to', 'in', 'it', 'is', 'be', 'as', 'at', 'so', 'we', 'he', 'by', 'or', 'on', 'do', 'if', 'me',
               'my', 'up', 'an', 'go', 'no', 'us', 'am']

three_letters = ['the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'any', 'can', 'had', 'her', 'was', 'one',
                 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'man', 'new', 'now', 'old', 'see', 'two',
                 'way', 'who', 'boy', 'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use']

four_letters = ['that', 'with', 'have', 'this', 'will', 'your', 'from', 'they', 'know', 'want', 'been', 'good', 'much',
                'some', 'time']


# function that sets cipher key dictionary with given letter and likely key for that
def set_letter(encrypted_letter, original_letter):
    cipher_key[encrypted_letter] = original_letter


# function returns the key for a given value in a dictionary
def get_key_by_value(val_to_be_found, given_dict):
    for key, value in given_dict.items():
        if value == val_to_be_found:
            return key


# we assume that most frequent letter is encrypted blank
def find_blank():
    last = ''
    before_last = ''
    maybe_blank = []
    maybe_a_or_i_patterns = []

    for character in file:
        if before_last == character and last != character:
            pattern = before_last + last + character
            maybe_blank.append(character)
            maybe_a_or_i_patterns.append(pattern)

        before_last = last
        last = character

    most_frequent_letter = ''
    for letter in maybe_blank:
        if most_frequent_letter:
            if maybe_blank.count(letter) > maybe_blank.count(most_frequent_letter):
                most_frequent_letter = letter
        else:
            most_frequent_letter = letter

    set_letter(most_frequent_letter, ' ')
    print("now we know that our blank is: " + most_frequent_letter)

    temp = []
    frequency_temp = {}
    for pattern in maybe_a_or_i_patterns:
        # find blank followed by any letter followed by blank - must be I or A
        regex = most_frequent_letter + r'.' + most_frequent_letter
        match = re.match(regex, pattern)
        if match:
            string = match.group(0)
            curr_letter = string.replace(most_frequent_letter, "")
            if curr_letter not in temp:
                temp.append(string.replace(most_frequent_letter, ""))

    for candidate in temp:
        frequency_temp[candidate] = file.count(candidate) / len(file)
        # set to remember
        letter_candidates[candidate] += 'a'
        letter_candidates[candidate] += 'i'

    # we now that "a" is more frequent in english texts than "i" so we are going to set the more frequent
    # letter to be the "a" letter
    frequency_temp_sorted = sorted(frequency_temp.items(), key=operator.itemgetter(1), reverse=True)
    print(frequency_temp_sorted)
    from operator import itemgetter
    most_frequent = itemgetter(1)(frequency_temp_sorted)[0]
    second_most_frequent = itemgetter(-2)(frequency_temp_sorted)[0]
    set_letter(most_frequent, 'a')
    set_letter(second_most_frequent, 'i')


# function that returns the letter which is defined as blank
def get_blank():
    for key, value in cipher_key.items():
        if value == ' ':
            return key
    blank = " "
    return blank


# function counts letters and sets the most frequent letter to "e" in cipher key
def count_letters():
    file_length = len(file)

    for i in letters:
        occ = file.count(i)
        letter_occurrence[i] = occ
        letter_frequencies[i] = (occ / file_length) * 100

    sorted_dict = sorted(letter_frequencies.items(), key=operator.itemgetter(1), reverse=True)
    from operator import itemgetter
    most_frequent = itemgetter(1)(sorted_dict)[0]
    second_most_frequent = itemgetter(2)(sorted_dict)[0]

    if 'e' not in cipher_key.values():
        # most frequent letter is e
        if cipher_key[most_frequent] != '':
            set_letter(second_most_frequent, 'e')
        else:
            set_letter(most_frequent, 'e')


# function counts occurrences of bigrams an sets the most frequent to "of"
def analyse_two_letter_words():
    two_letter_words = frequency_analyis.get_n_letter_words(2, file, get_blank())
    occ = {}
    print(two_letter_words)
    # most common two letter word is "of" followed by to, in, it...
    for word in two_letter_words:
        occ[word[0]] = two_letter_words.count(word)

    sorted_list = sorted(occ.items(), key=operator.itemgetter(1), reverse=True)
    print(sorted_list)
    print("------------------------------------")
    if sorted_list:
        most_frequent = sorted_list[0][0]
        set_letter(most_frequent[0], 'o')
        set_letter(most_frequent[1], 'f')
        second_most_frequent = sorted_list[1][0]
        set_letter(second_most_frequent[0], 't')
        set_letter(second_most_frequent[1], 'o')


# function counts three letter words and sets the most frequent to "the"
# and sets letters of second most frequent word to "a" "n" and "d"
def analyse_three_letter_words():
    three_letter_words = frequency_analyis.get_n_letter_words(3, file, get_blank())
    occ = {}
    # most common three letter word is "the", followed by "and", "for" ,..
    for word in three_letter_words:
        occ[word[0]] = three_letter_words.count(word)

    sorted_list = sorted(occ.items(), key=operator.itemgetter(1), reverse=True)
    most_frequent = sorted_list[0][0]  # supposed to be "the"
    second_most_frequent = sorted_list[1][0]  # supposed to be "and"

    # most frequent word is "THE"
    if most_frequent[0]:
        set_letter(most_frequent[0], 't')

    if most_frequent[1]:
        set_letter(most_frequent[1], 'h')

    if 'e' not in cipher_key.values():
        if most_frequent[2]:
            set_letter(most_frequent[2], 'e')

    # second most frequent word is "AND"
    if second_most_frequent[0]:
        set_letter(second_most_frequent[0], 'a')
        # and now that we know which letter is a:
        # we can set I:
        for key, value in letter_candidates.items():
            if 'i' in value and key != second_most_frequent[0]:
                # set cipher key to be this values
                set_letter(key, 'i')

    if second_most_frequent[1]:
        set_letter(second_most_frequent[1], 'n')

    if second_most_frequent[2]:
        set_letter(second_most_frequent[2], 'd')


# gets four letter words and tries to find matching letters for "that" and "will"
# as they have a pretty unique word pattern. "that" is the only 4 letter word starting
# with the same letter. and will is one of the few 4 letter words ending with a double letter
def analyse_four_letter_words():
    four_letter_words = frequency_analyis.get_n_letter_words(4, file, get_blank())
    occ = {}
    print(four_letter_words)
    for word in four_letter_words:
        print(word)
        occ[word[0]] = four_letter_words.count(word)
        if word[0][0] == word[0][3]:
            print(word)
            print("this word must be 'that'")
            string = 'that'
            i = 0
            while i < 4:
                set_letter(word[0][i], string[i])
                i = i + 1

        if word[0][2] == word[0][3]:
            print(word)
            print("this word must be 'will'")
            string = 'will'
            i = 0
            while i < 4:
                set_letter(word[0][i], string[i])
                i = i + 1
        # have
        if get_key_by_value('h', cipher_key) == word[0][0] and get_key_by_value('a', cipher_key) == word[0][1] and get_key_by_value('e', cipher_key) == word[0][3]:
            set_letter(word[0][2], 'v')

        # this
        if word[:3] == str(get_key_by_value('t', cipher_key)) + str(get_key_by_value('h', cipher_key)) + str(get_key_by_value('i', cipher_key)):
            set_letter(word[0][3], 's')
        # time
        if (get_key_by_value('t', cipher_key) == word[0][0] and get_key_by_value('i', cipher_key) == word[0][1] and get_key_by_value('e', cipher_key) == word[0][3]):
            set_letter(word[0][2], 'm')


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
        if frequency.get(str(double)):
            frequency[str(double)] += 1
        else:
            frequency[str(double)] = 1

    # check: if last three letters in* then we can assume that the * letter is g
    words = file.split(get_blank())
    if get_key_by_value('i', cipher_key) and get_key_by_value('n', cipher_key):
        i = get_key_by_value('i', cipher_key)
        n = get_key_by_value('n', cipher_key)
        matches = []
        for word in words:
            m = re.search(i + n + '.', word)  # search pattern in + anything
            if m:
                matches.append(m.group(0))

        matches_counted = {}
        for match in matches:
            occ = matches.count(match)
            matches_counted[match] = occ

        print(matches_counted)
        matches_sorted = sorted(matches_counted.items(), key=operator.itemgetter(1), reverse=True)
        from operator import itemgetter
        if matches_sorted:
            ing = itemgetter(0)(matches_sorted)[0]
            print(ing[2])
            cipher_key[ing[2]] = 'g'


def output_word(word):
    output_string = ""
    for character in word:
        if cipher_key.get(character) or letter_candidates.get(character):
            if cipher_key.get(character):
                output_string += cipher_key.get(character)
            else:
                output_string += str(letter_candidates.get(character))
        else:
            output_string += '*'
    return output_string


# checks the current input and counts how many of the decrypted words exist
def check_word(word, counter, original_text, score):
    global cipher_key
    word = output_word(word)
    if dictionary.check(word):
        return
    else:
        if word.count("*") * 2 < len(word):
            if dictionary.suggest(word):
                suggestions = dictionary.suggest(word)

                # now check every suggested word, when we set the new letter, if it
                # improves the score
                for suggested_word in suggestions[:5]:
                    current_word = suggested_word.lower()

                    # only consider words which are the same length as original word
                    if len(current_word) == len(word):
                        indices = get_indices(word)
                        cipher_key_copy = cipher_key

                        # check word letter by letter
                        for index in indices:
                            letter_to_decrypt = current_word[index]

                            # if letter already has a value set
                            if letter_to_decrypt in cipher_key.values():
                                print(letter_to_decrypt)
                                print("...is already set...")
                                setting_value = get_key_by_value(letter_to_decrypt, cipher_key)
                                print(setting_value)
                                current_orig_word = original_text[counter]
                                original_value = cipher_key.get(setting_value)
                                print("original: ")
                                print(original_value)
                                set_letter(current_orig_word[index], letter_to_decrypt)
                                set_letter(setting_value, '')
                                new_score = check_score()

                                # if score does not get better set letter back to original
                                if new_score <= score:
                                    cipher_key[current_orig_word[index]] = ''
                                    cipher_key[setting_value] = original_value
                                    continue
                                else:
                                    return
                            # if letter does not have a value set
                            else:
                                current_orig_word = original_text[counter]
                                set_letter(current_orig_word[index], letter_to_decrypt)

                        new_score = check_score()
                        print("NEW SCORE: ")
                        print(output())
                        print(new_score)
                        print(cipher_key)
                        # if new score is less or equal than score before swapping letters, then
                        # we know that swapping is not improving our cipher key
                        if new_score <= score:
                            cipher_key = cipher_key_copy
                            continue
                        else:
                            return


# returns an array containing each letter of decrypted word
def get_indices(decrypted):
    indices = []
    counter = 0
    for char in decrypted:
        if char == "*":
            indices.append(counter)
            counter = 0
        counter += 1
    return indices


# function to check score
# the score is a number from 0 to words of the text
# if dictionary contains a word, it improves score by one
def check_score():
    score = 0
    decrypted_text = output()
    decrypted_text = decrypted_text.split(" ")
    for word in decrypted_text:
        # if dictionary check returns true - dictionary contains word
        if dictionary.check(word):
            score += 1
    return score


# when all letter and n-gram-analysis is done, decryption starts
# as long sa score does not match the number of words of input file
# function check_word is being called
def start_decrypting():
    print("Start decrypting...")
    score = check_score()
    original_text = file.split(get_blank())
    words_len = len(original_text)
    print(words_len)
    # as long as not all words are recognized as existing words
    while words_len != check_score():
        counter = 0
        for word in original_text:
            if score != words_len:
                check_word(word, counter, original_text, score)
                score = check_score()
                counter += 1


# function generates output with current cipher key
# for unset letters, a "*" is being appended
def output():
    output_string = ""
    for character in file:
        if character == " ":
            output_string += " "
        elif cipher_key.get(character) or letter_candidates.get(character):
            if cipher_key.get(character):
                output_string += cipher_key.get(character)
            else:
                output_string += str(letter_candidates.get(character))
        else:
            output_string += '*'
    return output_string


# function defines sequence of events to decrypt a given english text
def decrypt(given_file, given_dictionary):
    # if blank appears less or equals than 1, we know that blank has also been decrypted
    if len(given_file.split(" ")) <= 1:
        find_blank()

    count_letters()
    analyse_two_letter_words()
    analyse_three_letter_words()
    analyse_four_letter_words()
    analyse_patterns()
    start_decrypting()
    print(frequency_analyis.get_n_letter_words(2, given_file, get_blank()))
    print(output())
    print(file)
    #print(letter_candidates)
    #print(cipher_key)


# main function starts decryption
def main():
    decrypt(file, dictionary)


main()
