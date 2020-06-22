Purpose
=======

This code aims at demonstrating an use of services in python-for-android, and
communication between services and a kivy front end.

That examples uses the OSC protocol for simplicity and historical reasons,
(since an implementation was shipped with kivy historically, and a better one
is now available as third party). The OSC protocol makes things simple because
it's unconnected, you just send a message, and can forget about it. You bind
functions to messages you receive. It's simple enough for a lot of things, and
avoids the burden of maintaining a connection when both the service and front
end can be restarted any time.

The app is composed of the front-end, defined in src/main.py, and the back-end defined in src/service.py.

The service (back-end):
  - is defined in buildozer.spec, in the `services` line. Following the example syntax
  - is started by the application at startup time, and can be stopped/restarted from the UI.
  - sends the current date, as a string, every tenth of a second to the UI, on a '/date' address.
  - answers with a random string on the '/message' address when a message is sent to the '/ping' address on its side.

The UI (front-end):
  - is defined in main.py
  - allows stopping/restarting the backend.
  - sends the last received messages as a notification
  - allow to sent a '/ping' message to the backend, which will trigger a new notification.

Building:
  - You can also just run the `kivy/buildozer` docker image to build your project from any Linux computer.

  ```
  docker run -v $PWD:/project/ -w /project/ kivy/buildozer android debug
  ```

  Once it's completed, you should have a bin/ directory with the apk inside.
