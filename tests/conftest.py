import pytest

from development.PushPip.cow_say import Worker, Parser
from argparse import Namespace


@pytest.fixture
def worker_cow_say() -> Worker:
    return Worker()


@pytest.fixture
def namespace_cow_say() -> Namespace:
    parser = Parser()
    return parser.parse_args()
