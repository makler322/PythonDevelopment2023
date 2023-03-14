"""Module for first task."""

from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Union

from cowsay import cowsay, list_cows
from pydantic import BaseModel

from development import PushPip
from development.config import load_config


class Parser(BaseModel):
    """Parser class."""

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
        for arg in config_args:
            flag, flag_params = arg.values()
            self.parser.add_argument(flag, **flag_params)


class Worker(BaseModel):
    """Parser class."""

    def __init__(self, cow: str = 'default'):
        """
        Get params from config.

        Args:
            cow: Default cow params.
        """
        super().__init__()
        self.cow = cow
        self.print_elem = None

    def run(self, args: Namespace) -> Union[list[str], str]:
        """
        Run prog from config.

        Args:
            args: Name of parse prog.

        Returns:
            Elem for pint
        """
        self.cow = args.cowfile if args.cowfile in list_cows() else self.cow
        cowfile_path = args.cowfile if '/' in args.cowfile else None
        self.print_elem = list_cows() if args.list else cowsay(
            cow=self.cow,
            eyes=args.eyes[:2],
            cowfile=cowfile_path,
            wrap_text=args.wrapped,
            tongue=args.tongue[:2],
            width=args.width,
            preset=max(args.apearence),
            message=args.message,
        )

        return self.print_elem


if __name__ == '__main__':
    parser = Parser()
    worker = Worker()

    args = parser.parse_args()
    worker.run(args)
