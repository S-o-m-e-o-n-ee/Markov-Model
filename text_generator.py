# Imports the necessary components
from markov_model import MarkovModel
import stdio
import sys


# Entry point.
def main():

    # Accept command-line arguments k (int) and n (int).
    k = int(sys.argv[1])
    n = int(sys.argv[2])

    # Initialize text to text read from standard input using sys.stdin.read().
    text = sys.stdin.read()

    # Create a Markov model using text and k.
    m = MarkovModel(text, k)

    # Use the model to generate a random text of length n and starting with the first k characters of text.
    g = m.gen(text[0:k], n)

    # Write the random text to standard output.
    stdio.writeln(g)


if __name__ == '__main__':
    main()
