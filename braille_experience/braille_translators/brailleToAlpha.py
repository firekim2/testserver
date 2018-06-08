# Translate braille to alphabet based text.
from . import mapAlphaToBraille, mapBrailleToAlpha

CAPITAL = chr(10272)  # ⠠
NUMBER = chr(10300)  # ⠼
UNRECOGNIZED = '?'


def extract_words(string):
    # Split up a sentence based on whitespace (" ") and new line ("\n") chars.
    words = string.split(" ")
    result = []
    for word in words:
        temp = word.split("\n")
        for item in temp:
            result.append(item)
    return result


def trim(word):
    # Remove punctuation around a word.
    while len(word) is not 0 and word[0] not in mapBrailleToAlpha.letters \
            and word[0] not in mapBrailleToAlpha.contractions:
        word = word[1:]
    while len(word) is not 0 and word[-1] not in mapBrailleToAlpha.letters \
            and word[-1] not in mapBrailleToAlpha.contractions:
        word = word[:-1]
    return word


def numbers_handler(word):
    # Translate braille numbers to standard number notation.
    if word == "":
        return word
    result = ""
    is_number = False
    for i in range(0, len(word)):
        if word[i] == NUMBER:
            is_number = True
            continue
        if is_number and word[i] in mapBrailleToAlpha.numbers:
            result += mapBrailleToAlpha.numbers.get(word[i])
        else:
            result += word[i]
    return result


def fix_exceptions(string):
    # Fix exceptions where a braille symbol can have multiple meanings.
    result = []
    # Decipher whether "⠦" should be "“" or "?".
    for i in range(0, len(string)):
        if i-1 >= 0 and string[i] == "“" and string[i-1] in mapAlphaToBraille.letters:
            result.append("?")
        else:
            result.append(string[i])
    # Decipher whether "()" should be "(" or ")".
    open_bracket = False
    while ("()") in result:
        if open_bracket:
            result = result.replace("()", ")", 1)
        else:
            result = result.replace("()", "(", 1)
        open_bracket = not open_bracket
    return result


def word_to_alpha(word):
    # Convert a braille word to alphabet based text.
    if word in mapBrailleToAlpha.contractions:
        return mapBrailleToAlpha.contractions.get(word)
    else:
        result = ""
        for i in range(0, len(word)):
            if word[i] in mapBrailleToAlpha.letters:
                result += mapBrailleToAlpha.letters.get(word[i])
            elif word[i] in mapBrailleToAlpha.punctuation:
                result += mapBrailleToAlpha.punctuation.get(word[i])
        return result

def rebuild_alpha_word(trimmed_word, shavings, index, alpha):
    # Translate a trimmed braille word to alphabet based text then re-attach the shavings.
    word = trimmed_word
    if shavings == "":
        if trimmed_word in mapBrailleToAlpha.contractions:
            alpha.append(mapBrailleToAlpha.contractions.get(word))
        else:
            for i in range(0, len(word)):
                if trimmed_word[i] in mapBrailleToAlpha.letters:
                    alpha.append(mapBrailleToAlpha.letters.get(word[i]))
                elif trimmed_word[i] in mapBrailleToAlpha.punctuation:
                    alpha.append(mapBrailleToAlpha.punctuation.get(word[i]))
    else:
        for i in range(0, len(shavings)):
            if i == index and trimmed_word is not "":
                if trimmed_word in mapBrailleToAlpha.contractions:
                    alpha.append(mapBrailleToAlpha.contractions.get(word))
                else:
                    for j in range(0, len(word)):
                        if trimmed_word[j] in mapBrailleToAlpha.letters:
                            alpha.append(mapBrailleToAlpha.letters.get(word[j]))
                        elif trimmed_word[j] in mapBrailleToAlpha.punctuation:
                            alpha.append(mapBrailleToAlpha.punctuation.get(word[j]))
            if shavings[i] in mapBrailleToAlpha.punctuation:
                alpha.append(mapBrailleToAlpha.punctuation.get(shavings[i]))
            else:
                alpha.append(shavings[i])
        if index == len(shavings):  # If the shavings are all at the beginning.
            if trimmed_word in mapBrailleToAlpha.contractions:
                alpha.append(mapBrailleToAlpha.contractions.get(word))
            else:
                for i in range(0, len(word)):
                    if trimmed_word[i] in mapBrailleToAlpha.letters:
                        alpha.append(mapBrailleToAlpha.letters.get(word[i]))
                    elif trimmed_word[i] in mapBrailleToAlpha.punctuation:
                        alpha.append(mapBrailleToAlpha.punctuation.get(word[i]))
    return alpha

def recapital_letters_handler(alpha):
    # Capitalize letters after the capitalization escape code.
    new_alpha = []
    i = 0
    while i < len(alpha):
        if alpha[i] == "⠠" and alpha[i + 1][0] in mapAlphaToBraille.letters:
            new_alpha.append(' ')
            new_alpha.append(alpha[i + 1].upper())
            i = i + 2
            continue
        else:
            new_alpha.append(alpha[i])
        i = i + 1
    return new_alpha

def retranslate(string):
    alpha = []
    words = extract_words(string)
    for word in words:
        word = numbers_handler(word)
        trimmed_word = trim(word)  # Remove punctuation.
        untrimmed_word = word
        index = untrimmed_word.find(trimmed_word)
        shavings = untrimmed_word.replace(trimmed_word, "")
        alpha = rebuild_alpha_word(trimmed_word, shavings, index, alpha)
        alpha.append(' ')
    alpha = recapital_letters_handler(alpha[:-1])
    return fix_exceptions(alpha)
