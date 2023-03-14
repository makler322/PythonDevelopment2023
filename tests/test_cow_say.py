from development.PushPip.cow_say import Worker
from argparse import Namespace


def test_dummy(worker_cow_say: Worker):
    args = Namespace()
    dummy_cow = worker_cow_say.run(args)
    assert dummy_cow == 1


def test_default(worker_cow_say: Worker, default_cow_params: Namespace):
    args = default_cow_params
    default_cow = worker_cow_say.run(args)
    assert default_cow == 1
