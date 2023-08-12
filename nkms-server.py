#!/usr/bin/python3

import argparse
import socketserver
import json
import asyncio
import evdev
import threading

toggle_key_down = False
socket_index = 0
sockets = []


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        while 1:
            if self.request not in sockets:
                sockets.append(self.request)

            self.request.send(b'test')

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



def get_next_socket():
    global socket_index
    if socket_index == len(sockets)-1:
        socket_index = 0
    else:
        socket_index = socket_index+1


async def start_tcp_server(address, port):
    with ThreadedTCPServer((address, port), ThreadedTCPRequestHandler) as server:
        server.allow_reuse_address = True
        # server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_thread = threading.Thread(target=server.serve_forever())
        server_thread.daemon = True
        server_thread.start()


async def handle_events(device):
    print(1)
    global socket_index, toggle_key_down
    async for event in device.async_read_loop():
        if event.code == 127:
            if toggle_key_down:
                # Context menu key
                get_next_socket()
            toggle_key_down = not toggle_key_down
        elif event.code == 88:
            # F12
            #mouse.ungrab()
            #keyboard.ungrab()
            exit()
        else:
            data = [event.type, event.code, event.value]
            print(data)
            if sockets:
                sock = sockets[socket_index]
                if sock:
                    sock.send(bytes(f"{json.dumps(data)}\n", "utf-8"))
            #sock.sendto(bytes(f"{json.dumps(data)}\n", "utf-8"), (addresses[address_index], port))


def get_km_devices():
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

    port = int(args.port)
    address = args.address

    km_devs = get_km_devices()
    for device in km_devs:
        km_dev = evdev.InputDevice(device.path)
        # km_dev.grab()
        print(device.path)
        asyncio.ensure_future(handle_events(km_dev))

    asyncio.ensure_future(start_tcp_server(address, port))

    loop = asyncio.get_event_loop()
    loop.run_forever()
