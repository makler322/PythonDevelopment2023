import pytest

from development.PushPip.cow_say import Worker
from argparse import Namespace


@pytest.fixture
def worker_cow_say() -> Worker:
    return Worker()


@pytest.fixture
def default_cow_params() -> Namespace:
    return Namespace(e="xx", T="SS", W=60)
