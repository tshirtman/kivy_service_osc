__version__ = '0.1'

from kivy.app import App
from kivy.lang import Builder
from kivy.lib import osc
from kivy.clock import Clock
from kivy.utils import platform
platform = platform()

kv = '''
BoxLayout:
    orientation: 'vertical'
    BoxLayout:
        size_hint_y: None
        height: '30sp'
        Button:
            text: 'start service'
            on_press: app.start_service()
        Button:
            text: 'stop service'
            on_press: app.stop_service()

    ScrollView:
        Label:
            id: label
            size_hint_y: None
            height: self.texture_size[1]
            text_size: self.size[0], None

    BoxLayout:
        size_hint_y: None
        height: '30sp'
        Button:
            text: 'ping'
            on_press: app.send()
        Button:
            text: 'clear'
            on_press: label.text = ''
        Label:
            id: date

'''


class ClientServerApp(App):
    def build(self):
        self.service = None
        self.start_service()
        osc.init()
        oscid = osc.listen(port=3002)
        osc.bind(oscid, self.display_message, '/message')
        osc.bind(oscid, self.date, '/date')
        Clock.schedule_interval(lambda *x: osc.readQueue(oscid), 0)
        self.root = Builder.load_string(kv)
        return self.root

    def start_service(self):
        if platform == 'android':
            from android import AndroidService
            service = AndroidService('my pong service', 'running')
            service.start('service started')
            self.service = service

    def stop_service(self):
        if self.service:
            self.service.stop()
            self.service = None

    def send(self, *args):
        osc.sendMsg('/ping', [], port=3000)

    def display_message(self, message, *args):
        if self.root:
            self.root.ids.label.text += '%s\n' % message[2]

    def date(self, message, *args):
        if self.root:
            self.root.ids.date.text = message[2]


if __name__ == '__main__':
    ClientServerApp().run()
