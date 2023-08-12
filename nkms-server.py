#!/usr/bin/python3

import argparse
import socketserver
import json
import evdev
import threading

toggle_key_down = False
grabbing = False
grab_status = {}
socket_index = -1
sockets = []


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        while 1:
            if self.request not in sockets:
                sockets.append(self.request)
                print(f'New connection: {self.request}')

            # self.request.send(bytes(f"{json.dumps(caps)}\n", "utf-8"))

            data = self.request.recv(1024)
            if not data:
                break

            # data = json.loads(data.strip())
            # if not data:
            #    continue

            print(data)
            print(sockets)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):

    def server_bind(self):
        self.allow_reuse_address = True
        super(ThreadedTCPServer, self).server_bind()


def start_tcp_server(address, port):
    with ThreadedTCPServer((address, port), ThreadedTCPRequestHandler) as server:
        server.allow_reuse_address = True
        server.serve_forever()


def get_next_socket():
    """
    Set socket_index to next value to cycle through outputs
    """
    global socket_index, grabbing

    if socket_index == len(sockets)-1:
        socket_index = -1
        grabbing = False
    else:
        socket_index = socket_index+1
        grabbing = True


def do_grabbing(grab_dev):
    """
    Grab / Ungrab device depending on value of `grabbing`
    Also set status in `grab_status` since there's not an easy way
    to check a devices grab status
    """
    if grabbing and grab_status[grab_dev.path] is False:
        grab_dev.grab()
        grab_status[grab_dev.path] = True
    elif not grabbing and grab_status[grab_dev.path] is True:
        grab_dev.ungrab()
        grab_status[grab_dev.path] = False


def handle_events(device):
    """
    Start loop to listen for device's events
    """
    global socket_index, toggle_key_down, grabbing
    for event in device.async_read_loop():
        do_grabbing(device)
        if event.code == 127:
            # Context menu key
            if toggle_key_down:
                get_next_socket()
            toggle_key_down = not toggle_key_down
        else:
            data = [event.type, event.code, event.value]
            # print(data)
            if sockets and socket_index >= 0:
                sock = sockets[socket_index]
                try:
                    sock.send(bytes(f"{json.dumps(data)}\n", "utf-8"))
                except OSError:
                    print(f'Dropped connection: {sock}')
                    del sockets[socket_index]
                    socket_index = -1
                    grabbing = False


def get_km_devices():
    """
    Get devices that have capabilities that look like a keyboard or mouse
    """
    devs = []
    all_devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for dev in all_devices:
        cap = dev.capabilities()
        ec = evdev.ecodes
        if ec.EV_KEY in cap:
            keys = cap[ec.EV_KEY]
            if ec.BTN_LEFT in keys or (ec.KEY_A in keys and ec.KEY_Z in keys):
                devs.append(dev)
    return devs


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Network Keyboard and Mouse Switch')
    parser.add_argument('--address', '-a', type=str, help='port to listen on', default='0.0.0.0')
    parser.add_argument('--port', '-p', type=str, help='port to listen on', default=4777)
    args = parser.parse_args()

    print('Starting NKMS Server ...')
    port = int(args.port)
    address = args.address

    print('Loading input devices ...')
    km_devs = get_km_devices()
    threads = []
    for device in km_devs:
        km_dev = evdev.InputDevice(device.path)
        print(device.path)
        grab_status[device.path] = False
        thread = threading.Thread(target=handle_events, args=(km_dev,))
        thread.start()
        threads.append(thread)

    print('Starting TCP server ...')
    tcp_thread = threading.Thread(target=start_tcp_server, args=(address, port,))
    tcp_thread.start()
    threads.append(tcp_thread)

    print('Running ...')
    for thread in threads:
        thread.join()
