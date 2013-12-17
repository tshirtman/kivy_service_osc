from kivy.lib import osc
from random import sample, randint
from string import ascii_letters
from time import localtime, asctime, sleep


def ping(*args):
    osc.sendMsg(
        '/message',
        [''.join(sample(ascii_letters, randint(10, 20))), ],
        port=3002)


def send_date():
    osc.sendMsg('/date', [asctime(localtime()), ], port=3002)


if __name__ == '__main__':
    osc.init()
    oscid = osc.listen(ipAddr='0.0.0.0', port=3000)
    osc.bind(oscid, ping, '/ping')
    while True:
        osc.readQueue(oscid)
        send_date()
        sleep(.1)
