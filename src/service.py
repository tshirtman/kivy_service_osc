from random import sample, randint
from string import ascii_letters
from time import localtime, asctime, sleep

from oscpy.server import OSCThreadServer
from oscpy.client import OSCClient

client = OSCClient('localhost', 3002)

def ping(*args):
    client.send_message(
        b'/message',
        [
            ''.join(sample(ascii_letters, randint(10, 20)))
            .encode('utf8'),
        ],
    )


def send_date():
    client.send_message(
        b'/date',
        [asctime(localtime()).encode('utf8'), ],
    )


if __name__ == '__main__':
    server = OSCThreadServer()
    server.listen('localhost', port=3000, default=True)
    server.bind(b'/ping', ping)
    while True:
        sleep(1)
        send_date()
