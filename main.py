import json
from time import *

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'


with open("sorted_dict.json") as f:
    words = json.load(f)


def set_word_pool(length):
    return words[str(length)]


# Checks if the given word exists in the dictionary
def valid_word(word):
    for key in words:
        if word in words[key]:
            return True


def dict_sort(dict_name):
    dict = dict_loader(dict_name)
    sorted_dict = {}

    for word in dict:
        word_length = int(len(word))

        if word_length in sorted_dict:
            sorted_dict[word_length].append(word)
        else:
            sorted_dict[word_length] = [word]

    return sorted_dict


def print_possible_words(word_pool):
    print("Possible words: ", end="")
    if len(word_pool) > 10:
        for word in word_pool:
            print(word, end="")
            if word == word_pool[9]:
                print(" and {} more!".format(len(word_pool) - 10))
                break
            else:
                print(", ", end="")
    else:
        for word in word_pool:
            print(word, end="")
            if word == word_pool[-1]:
                print("")
                break
            else:
                print(" ,", end="")


def dict_create(dict, dict_name = 'new_dict.json'):
    with open(dict_name, 'w') as f:
        json.dump(dict, f, indent=4)


# Gets the most popular letter in the given word pool
def getPopularLetter(wordPool, guessedLetters, onlyTable=False):
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    # Create table for letter frequencies
    table = {}
    for letter in alphabet:
        table.update({letter: 0})

    # Count letter appearances
    for letter in alphabet:
        for word in wordPool:
            if letter in word:
                table[letter] += 1

    # Exclude all guessed letters from the table
    for item in list(table.items()):
        if item[0] in guessedLetters:
            table.update({item[0]: -10})

    if onlyTable:
        return table

    # Find the most popular letter among the table
    maxPopularity = -10
    for item in list(table.items()):
        if item[1] > maxPopularity:
            maxPopularity = item[1]
            popularLetter = item[0]

    return popularLetter


def most_common_letter(word_pool, already_guessed):
    global ALPHABET

    highest_freq = 0
    for char in ALPHABET:
        if char in already_guessed:
            continue

        count = 0
        freq = 0
        for word in word_pool:
            if char in word:
                count += 1

        freq = count / len(word_pool)
        if freq > highest_freq:
            highest_freq = freq
            guess = char

    return guess


def update_revealed(revealed, guess, word):
    for i in range(len(revealed)):
        if word[i] == guess:
            revealed[i] = guess

    return revealed


def render_revealed(revealed):
    revealed_text = ""
    for i in range(len(revealed)):
        if revealed[i] is None:
            revealed_text += "_"
        else:
            revealed_text += revealed[i]

    return revealed_text


def comparison_prune(word_pool, guess, revealed):
    for word in word_pool[:]:
        for i in range(len(revealed)):
            if revealed[i] is None:
                if word[i] == guess:
                    word_pool.remove(word)
                    break
            elif revealed[i] != word[i]:
                word_pool.remove(word)
                break

    return word_pool


# Removes all words in word pool that contain a given letter
def false_prune(word_pool, letter):
    for word in word_pool[:]:
        if letter in word:
            word_pool.remove(word)

    return word_pool


# Input a word for the AI to guess
def choose_word():
    word = input("\nChoose a word for the AI to guess: ").lower()

    if valid_word(word):
        return word
    else:
        print("\nThat word is not in the dictionary!")


def hangman(word):

    print("\nI am analyzing the word...")
    sleep(.2)


    mistakes = 0
    revealed = [None] * len(word)
    letters_guessed = []
    total_guesses = 0


    word_pool = set_word_pool(len(word))

    while None in revealed:

        guess = getPopularLetter(word_pool, letters_guessed)
        total_guesses += 1
        print("\nI guess the letter {}!".format(guess))
        print("Total guesses:", total_guesses)


        if guess in word:
            revealed = update_revealed(revealed, guess, word)
            word_pool = comparison_prune(word_pool, guess, revealed)
        else:
            mistakes += 1
            word_pool = false_prune(word_pool, guess)

        print("Mistakes:", mistakes)
        print(render_revealed(revealed))
        sleep(.2)

        letters_guessed.append(guess)

    if mistakes > 1:
        print("The AI guessed the word within {} mistakes!".format(mistakes))
    elif mistakes == 1:
        print("The AI guessed the word only within {} mistake!".format(mistakes))
    else:
        print("The AI guessed the word without mistakes!")


if __name__ == "__main__":

    word = choose_word()
    while word is None:
        word = choose_word()
    hangman(word)


