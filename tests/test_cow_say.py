from src.PushPip.cow_say import Worker
from argparse import Namespace


def test_default(namespace_cow_say: Namespace, worker_cow_say: Worker):
    dummy_cow = worker_cow_say.run(namespace_cow_say)
    assert dummy_cow == ' ___ \n' + \
                        '<   >\n' + \
                        ' --- \n' + \
                        '        \\   ^__^\n' + \
                        '         \\  (oo)\\_______\n' + \
                        '            (__)\\       )\\/\\\n' + \
                        '              ||----w |\n' + \
                        '                ||     ||'
