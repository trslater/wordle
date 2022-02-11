"""Wordle"""

from argparse import ArgumentParser
from pathlib import Path
import random
import sys


def main():
    """CLI entrypoint"""

    # Parse args
    parser = ArgumentParser(description="The great game of wordle")
    parser.add_argument("--solution", help="sets the solution to SOLUTION")
    args = parser.parse_args()

    # Load word list
    abs_path = Path(__file__, "..").resolve()
    with open(abs_path/"data/words.txt") as words_file:
        words = tuple(map(str.strip, words_file))
    
    wordle = Wordle(words, args.solution or random.choice(words))

    while wordle.is_playing:
        try:
            guess = input("Guess: ")
        
        except KeyboardInterrupt:
            sys.exit(0)

        try:
            print(", ".join(f"{c}: {status}"
                            for c, status
                            in zip(guess, wordle.clues(guess))))

        except WordNotInListError:
            print("Word not in list...")

        except GameWonException:
            print("You won!")
            sys.exit(0)

        except GameLostException:
            print("You lost :(")
            sys.exit(0)

        else:
            print(f"You have {wordle.turns_left} turns left")


class Wordle:
    """Main game class"""

    def __init__(self, words, solution) -> None:
        self.words = words
        self.solution = solution
        self.is_playing = True
        self.turns_left = 6

    def clues(self, guess: str) -> tuple[tuple[str, str]]:
        """Given a guess, return clues about your guess"""

        if guess not in self.words:
            raise WordNotInListError()

        if guess == self.solution:
            self.is_playing = False
            raise GameWonException()

        # If we only have one turn left, hints are useless, quit right away
        if self.turns_left <= 1:
            self.is_playing = False
            raise GameLostException()

        letter_status = [None]*5

        for i, (a, b) in enumerate(zip(guess, self.solution)):
            if a == b:
                letter_status[i] = "correct"
            
            elif a in self.solution:
                letter_status[i] = "present"
            
            else:
                letter_status[i] = "absent"

        self.turns_left -= 1

        return letter_status


class WordNotInListError(Exception):
    """The word chosen was not in the provided list of words"""


class GameWonException(Exception):
    """Signifies a won game event"""


class GameLostException(Exception):
    """Signifies a lost game event"""


if __name__ == "__main__":
    main()
