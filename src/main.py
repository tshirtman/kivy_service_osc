# coding: utf8
__version__ = '0.2'

from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.utils import platform

from jnius import autoclass

from oscpy.client import OSCClient
from oscpy.server import OSCThreadServer


SERVICE_NAME = u'{packagename}.Service{servicename}'.format(
    packagename=u'org.kivy.oscservice',
    servicename=u'Pong'
)

KV = '''
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
        # self.start_service()

        self.server = server = OSCThreadServer()
        server.listen(
            address=b'localhost',
            port=3002,
            default=True,
        )

        server.bind(b'/message', self.display_message)
        server.bind(b'/date', self.date)

        self.client = OSCClient(b'localhost', 3000)
        self.root = Builder.load_string(KV)
        return self.root

    def start_service(self):
        if platform == 'android':
            service = autoclass(SERVICE_NAME)
            self.mActivity = autoclass(u'org.kivy.android.PythonActivity').mActivity
            argument = ''
            service.start(self.mActivity, argument)
            # service.start(self.mActivity, 'small_icon', 'title', 'content' , argument)
            self.service = service
            
            # # Service restart
            # # https://python-for-android.readthedocs.io/en/latest/services/
            # self.service.mActivity.setAutoRestartService(True)

        elif platform in ('linux', 'linux2', 'macos', 'win'):
            from runpy import run_path
            from threading import Thread
            self.service = Thread(
                target=run_path,
                args=['src/service.py'],
                kwargs={'run_name': '__main__'},
                daemon=True
            )
            self.service.start()
        else:
            raise NotImplementedError(
                "service start not implemented on this platform"
            )

    def stop_service(self):
        if self.service:
            if platform == "android":
                self.service.stop(self.mActivity)
            elif platform in ('linux', 'linux2', 'macos', 'win'):
                # The below method will not work. 
                # Need to develop a method like 
                # https://www.oreilly.com/library/view/python-cookbook/0596001673/ch06s03.html
                self.service.stop()
            else:
            	raise NotImplementedError(
                	"service start not implemented on this platform"
            	)
            self.service = None

    def send(self, *args):
        self.client.send_message(b'/ping', [])

    def display_message(self, message):
        if self.root:
            self.root.ids.label.text += '{}\n'.format(message.decode('utf8'))

    def date(self, message):
        if self.root:
            self.root.ids.date.text = message.decode('utf8')


if __name__ == '__main__':
    ClientServerApp().run()
