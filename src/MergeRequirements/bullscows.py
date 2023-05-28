"""Module for second task."""

import sys
from collections import defaultdict
from pathlib import Path
from random import choice
from typing import Callable, List

from pydantic import BaseModel

from src import MergeRequirements
from src.PushPip.cow_say import Parser


class Worker(BaseModel):
    """Worker class."""

    words: List[str] = []

    def __init__(self, valid_filename: str = None):
        """
        Get params from config.

        Args:
            valid_filename: Path of valid filename
        """
        super().__init__()
        valid_filename = valid_filename if valid_filename else 'valid.txt'
        self._get_words(valid_filename)

    def gameplay(
        self,
        words: List[str] = None,
        ask: Callable[[str, List[str]], str] = None,
        inform: Callable[[str, int, int], None] = None,
    ) -> int:
        """
        Start main gameplay.

        Args:
            words: Valid words.
            ask: Ask func.
            inform: Print func.
        Returns:
            Nums of trying.
        """
        words = words if words else self.words
        ask = ask if ask else self._ask
        inform = inform if inform else self._inform
        secret = choice(words)

        count = 0
        guess = ''
        while guess != secret:
            guess = ask("Input word: ", words)
            count += 1
            bulls, cows = self._bullscows(guess, secret)
            inform("Bulls {}, Cows {}", bulls, cows)
        return count

    def _ask(self, prompt: str, valid: List[str] = None) -> str:
        """
        Start main gameplay.

        Args:
            prompt: Invite msg.
            valid: Valid list.
        Returns:
            str: Nums of trying.
        """
        word = input(prompt)
        if valid:
            while word not in valid:
                sys.stdout.write(f"{word} not in valid list!")
                word = input(prompt)
        return word

    def _bullscows(self, guess: str, secret: str) -> (int, int):
        """
        Main computing function.

        Args:
            guess: input msg.
            secret: correct msg.
        Returns:
            (int, int): Nums of bulls and cows.
        """
        guess_dict = defaultdict(int)
        secret_dict = defaultdict(int)

        for let_guess, let_secret in zip(guess, secret):
            guess_dict[let_guess] += 1
            secret_dict[let_secret] += 1

        bulls_arr = [let_guess == let_secret for let_guess, let_secret in zip(guess, secret)]
        bulls = sum(bulls_arr)
        cows_arr = [min(value, guess_dict[key]) for (key, value) in secret_dict.items()]
        cows = sum(cows_arr)
        cows -= bulls
        return bulls, cows

    def _inform(self, format_string: str, bulls: int, cows: int) -> None:
        sys.stdout.write(format_string.format(bulls, cows))

    def _get_words(self, valid_filename: str) -> None:
        self.words = []
        with open(valid_filename, 'r') as open_file:
            for line in open_file.readlines():
                line_strip = line.strip()
                if len(line_strip) == args.length:
                    self.words.append(line_strip)


if __name__ == '__main__':
    parser = Parser(
        prog='bullscows',
        description='bulls and cows',
        args_path=Path(MergeRequirements.__file__).parent / 'config.yml',
    )
    args = parser.parse_args()
    worker = Worker(args.dictionary)
    worker.gameplay()
