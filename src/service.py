'p4a example service using oscpy to communicate with main application.'
from random import sample, randint
from string import ascii_letters
from time import localtime, asctime, sleep

from oscpy.server import OSCThreadServer
from oscpy.client import OSCClient

CLIENT = OSCClient('localhost', 3002)


def ping(*_):
    'answer to ping messages'
    CLIENT.send_message(
        b'/message',
        [
            ''.join(sample(ascii_letters, randint(10, 20)))
            .encode('utf8'),
        ],
    )


def send_date():
    'send date to the application'
    CLIENT.send_message(
        b'/date',
        [asctime(localtime()).encode('utf8'), ],
    )


if __name__ == '__main__':
    SERVER = OSCThreadServer()
    SERVER.listen('localhost', port=3000, default=True)
    SERVER.bind(b'/ping', ping)
    while True:
        sleep(1)
        send_date()
