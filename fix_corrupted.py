# Imports the necessary components
from markov_model import MarkovModel
import stdio
import sys


# Entry point.
def main():

    # Accepts k (int) and corrupted (str) as command-line arguments.
    k = int(sys.argv[1])
    corrupted = sys.argv[2]

    # Initializes text to text read from standard input using sys.stdin.read().
    text = sys.stdin.read()

    # Creates a Markov model using text and k.
    m = MarkovModel(text, k)

    # Uses the model to decode corrupted.
    a = m.replace_unknown(corrupted)

    # Writes the decoded text to standard output.
    stdio.writeln(a)


if __name__ == '__main__':
    main()
