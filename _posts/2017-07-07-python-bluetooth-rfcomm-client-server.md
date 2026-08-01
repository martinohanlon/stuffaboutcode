---
title: 'Python Bluetooth RFCOMM Client Server'
date: 2017-07-07 15:37:00 +01:00
tags: [python, raspberry-pi]
redirect_from:
  - /2017/07/python-bluetooth-rfcomm-client-server.html
---

As part of the [Blue Dot](http://www.stuffaboutcode.com/2017/04/bluedot-bluetooth-remote-for-raspberry.html) project I needed to create a simple Bluetooth client / server library so that the communication could be managed. This library, [btcomm](http://bluedot.readthedocs.io/en/latest/btcommapi.html), is part of bluedot but its not exclusive and can be used for Bluetooth communication in Python.

It uses a 2 way RFCOMM communication - you can send messages to and from 2 devices, 1 being the server which waits for connections, 1 being the client which makes a connection.

**Install the library**

```bash
sudo apt-get install python3-dbus
sudo pip3 install bluedot
```

**Pairing**

The 2 devices you which want to communicate between will need to be paired, the Blue Dot documentation describes [how to pair 2 raspberry pi's](http://bluedot.readthedocs.io/en/latest/pairpipi.html) which might be useful.

**Simple Client / Server Example**

Lets create a simple example, a server which waits for connections and when it receives data it echo's it back to the client.

Create a new Python program and save it as btserver.py:

```python
from bluedot.btcomm import BluetoothServer
from signal import pause

def data_received(data):
    print(data)
    s.send(data)

s = BluetoothServer(data_received)
pause()
```

Create a 2nd program and save it as btclient.py:

```python
from bluedot.btcomm import BluetoothClient
from signal import pause

def data_received(data):
    print(data)

c = BluetoothClient("nameofyourserver", data_received)
c.send("helloworld")

pause()
```

Run the server and then run the client, the client should connect and "Hello World" will be sent to the server and displayed on the screen, the server will then send the same "Hello World" message back to the client, which will print it to the screen.

**Adapter**

There is also a useful API for accessing the Bluetooth adapter allowing you to get its current status, power it on/off, make it discoverable or find the devices its paired with.

```python
from bluedot.btcomm import BluetoothAdapter

a = BluetoothAdapter()

print("Powered = {}".format(a.powered))
print(a.paired_devices)
a.allow_pairing()
```

**Documentation**

There is comprehensive documentation for the [btcomm library](http://bluedot.readthedocs.io/en/latest/btcommapi.html), which describes the API and how to use it.
