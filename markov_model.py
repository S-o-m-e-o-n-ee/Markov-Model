# Imports the necessary components
from symboltable import SymbolTable
import stdio
import stdrandom
import sys


class MarkovModel(object):
    # Creates a Markov model of order k from the given text.
    def __init__(self, text, k):

        # Stores the order of the model
        self._k = k

        # Creates a symbol table used to keep track of the values in the model
        self._st = SymbolTable()

        # Creates a text that allows for the comparison of the first and last characters
        circ_text = text + text[0] + text[1]

        # Repeats over all of circ_text except the last character
        for i in range(len(circ_text) - k):

            # Sets the kgram to the k characters after i
            kgram = circ_text[i:i + k]

            # Sets next_char to the character that follows the kgram
            next_char = circ_text[i + k]

            # If kgram is already in self._st, either adds one to the corresponding value in self._st[kgram] or creates
            # a new value, otherwise creates a self._st[kgram] and the corresponding value for next_char
            if kgram in self._st:

                # Setts a to the previous value that was in self._st[kgram]
                a = self._st[kgram]

                # If next_char is already in a, adds one to the value, otherwise creates a new value for a[next_char]
                if next_char in a:
                    a[next_char] += 1
                else:
                    a[next_char] = 1

                # Sets self._st[kgram] to the updated value using a
                self._st[kgram] = a
            else:
                a = SymbolTable()
                a[next_char] = 1
                self._st[kgram] = a

    # Returns the order this Markov model.
    def order(self):
        return self._k

    # Returns the number of occurrences of kgram in this Markov model; and 0 if kgram is
    # nonexistent. Raises an error if kgram is not of length k.
    def kgram_freq(self, kgram):

        # Raises an error if kgram is not of length k
        if self._k != len(kgram):
            raise ValueError('kgram ' + kgram + ' not of length ' + str(self._k))

        # Returns 0 if kgram is not in self._st
        if kgram not in self._st:
            return 0

        # Creates a counter variable
        count = 0

        # Adds up all of the occurrences in self._st[kgram]
        for i in self._st[kgram].values():
            count += i

        # Returns the number of occurrences of kgram in the model
        return count

    # Returns number of times character c follows kgram in this Markov model; and 0 if kgram is
    # nonexistent or if it is not followed by c. Raises an error if kgram is not of length k.
    def char_freq(self, kgram, c):

        # Raises an error if kgram is not of length k
        if self._k != len(kgram):
            raise ValueError('kgram ' + kgram + ' not of length ' + str(self._k))

        # Returns 0 if kgram does not exist in self._st
        if kgram not in self._st:
            return 0

        # Returns 0 if c does not exist in self._st[kgram]
        if c not in self._st[kgram]:
            return 0

        # Returns number of times character c follows kgram in the model
        return self._st[kgram][c]

    # Returns a random character following kgram in this Markov model. Raises an error if kgram is
    # not of length k or if kgram is nonexistent.
    def rand(self, kgram):

        # Raises an error if kgram is not of length k
        if self._k != len(kgram):
            raise ValueError('kgram ' + kgram + ' not of length ' + str(self._k))

        # Raises an error if kgram is nonexistent
        if kgram not in self._st:
            raise ValueError('Unknown kgram ' + kgram)

        # Creates the alias a for self._st[kgram]
        a = self._st[kgram]

        # Creates an empty list b
        b = []

        # Iterates over all the keys in a
        for i in a.values():
            # Adds the probability of that each value will appear after kgram to the list b
            b += [i / self.kgram_freq(kgram)]

        # Uses the probability from b to get a random number
        rand = stdrandom.discrete(b)

        # Find the character corresponding to the random value
        x = 0
        rand_char = "error"
        for i in a.keys():
            if x == rand:
                rand_char = i
            x += 1

        # Returns the random character
        return rand_char

    # Generates and returns a string of length n from this Markov model, the first k characters of which is kgram.
    def gen(self, kgram, n):

        # Initializes the string to just kgram
        the_string = kgram

        # Initializes the variables for the next section
        new_kgram = kgram
        i = 0
        x = 0
        a = []

        # Adds a new character to the string using the kgram that comes before it
        while len(the_string) < n:

            # Creates an indicator variable
            did_we_hit_error = False

            # Sets rand_char, a possible new character to be added to the_string, to a random character
            rand_char = self.rand(new_kgram)

            # Creates a variable possibility that is what the_string would be if rand_char was added
            possibility = the_string + rand_char

            # If the kgram from the end of possibility does not exist in self._st...
            if possibility[1 + i: self._k + 1 + i] not in self._st:

                # Increments the counter variable x
                x += 1

                # If the previous code has been run 100 times, subtracts the last k letters of the_string and adds a
                # random kgram from self._st and changes the indicator variable to True, otherwise uses the continue
                # keyword
                if x > 100:
                    the_string = the_string[0: len(the_string) - self._k + 1]
                    for y in self._st.keys():
                        a += [y]
                    the_string += a[stdrandom.uniformInt(0, len(a))]
                    did_we_hit_error = True
                else:
                    continue

            # If the indicator variable is still false, adds rand_char to the_string
            if not did_we_hit_error:
                the_string += rand_char

            # Resets the variable new_kgram as the kgram from the end of the_string
            new_kgram = the_string[1 + i: self._k + 1 + i]

            # Increments the counter variable i
            i += 1

        # Returns the string
        return the_string

    # Replaces unknown characters (~) in corrupted with most probable characters from this Markov
    # model, and returns that string.
    def replace_unknown(self, corrupted):

        # Initializes original as an empty string
        original = ''

        # Iterates over all the index values in corrupted
        for i in range(len(corrupted)):

            # If the character is corrupted...
            if corrupted[i] == '~':

                # Setts the kgram before and after the corrupted character to variables
                kgram_before = corrupted[i - self._k:i]
                kgram_after = corrupted[i + 1: i + self._k + 1]

                # Creates a dictionary to store the probabilities and the corressponding characters
                probs = {"nothing": -20}

                # Iterates over every possible character that could replace the corrupted character
                for hypothesis in self._st[kgram_before].keys():

                    # Creates a test string of the kgrams before and after as well as the possible replacement value
                    context = kgram_before + hypothesis + kgram_after

                    # Initializes the probability to 1.0
                    p = 1.0

                    # Gathers the probability of the replacement character working
                    for x in range(0, self._k + 1):
                        kgram = context[x: x + self._k]
                        char = context[x + self._k]
                        if kgram in self._st and char in self._st[kgram]:
                            p *= (self.char_freq(kgram, char) / self.kgram_freq(kgram))
                        else:
                            p = 0
                            break

                    # Adds p and the corressponding character to probs
                    probs[hypothesis] = p

                # Finds the character with the highest probability of working
                a = []
                char = "error"
                for x in probs.values():
                    a += [x]
                for x in reversed(probs.keys()):
                    if probs[x] == max(a):
                        char = x

                # Appends the character most likely to replace the corrupter character
                original += char

            else:

                # Appends the not corrupted character from the corrupted text
                original += corrupted[i]

        return original


# Given a list a, _argmax returns the index of the maximum value in a.
def _argmax(a):
    return a.index(max(a))


# Unit tests the data type [DO NOT EDIT].
def _main():
    text = sys.argv[1]
    k = int(sys.argv[2])
    model = MarkovModel(text, k)
    a = []
    while not stdio.isEmpty():
        kgram = stdio.readString()
        char = stdio.readString()
        a.append((kgram.replace('-', ' '), char.replace('-', ' ')))
    for kgram, char in a:
        if char == ' ':
            stdio.writef('freq(%s) = %s\n', kgram, model.kgram_freq(kgram))
        else:
            stdio.writef('freq(%s, %s) = %s\n', kgram, char, model.char_freq(kgram, char))


if __name__ == '__main__':
    _main()
