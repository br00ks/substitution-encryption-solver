def output_word(word, cipher_key, letter_candidates):
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

