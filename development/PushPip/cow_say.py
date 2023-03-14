"""Module for first task."""

import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Any, Union

from cowsay import cowsay, list_cows
from pydantic import BaseModel

from development import PushPip
from development.config import load_config


class Parser(BaseModel):
    """Parser class."""

    parser: Any

    def __init__(
        self,
        prog: str = 'Cowsay',
        description: str = 'Cowsay imitation',
    ):
        """
        Get params from config.

        Args:
            prog: Name of parse prog.
            description: Description of parse prog.
        """
        super().__init__()
        self.parser = ArgumentParser(prog=prog, description=description)
        self._add_args()

    def parse_args(self) -> Namespace:
        """
        Parse args.

        Returns:
            Namespace: Object of parsing args.
        """
        return self.parser.parse_args()

    def _add_args(self):
        """Loop for adding args from config."""
        config_args = load_config(
            Path(PushPip.__file__).parent / 'config.yml',
        ).arguments
        for flag, flag_params in config_args.items():
            self.parser.add_argument(flag, **flag_params)


class Worker(BaseModel):
    """Parser class."""

    cow: str = 'default'

    def run(self, args: Namespace) -> Union[list[str], str]:
        """
        Run prog from config.

        Args:
            args: Name of parse prog.

        Returns:
            Elem for pint
        """
        cow = args.cowfile if args.cowfile in list_cows() else self.cow
        cowfile_path = args.cowfile if '/' in args.cowfile else None
        return cowsay(
            cow=cow,
            eyes=args.eyes[:2],
            cowfile=cowfile_path,
            wrap_text=args.wrap_text,
            tongue=args.tongue[:2],
            width=args.width,
            preset=max(args.preset),
            message=args.message,
        )


if __name__ == '__main__':
    parser = Parser()
    worker = Worker()

    args = parser.parse_args()
    sys.stdout.write(worker.run(args))
