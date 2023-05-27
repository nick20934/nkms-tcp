#!/usr/bin/python3

import argparse
import evdev
import socket
import json

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Keyboard and Mouse Event listener')
    parser.add_argument('--address', '-a', type=str, help='address to connect to', default='localhost')
    parser.add_argument('--port', '-p', type=str, help='port to connect to', default=4545)
    parser.add_argument('--mouse', '-m', type=str, help='mouse event', default='event7')
    parser.add_argument('--list', '-l', help='list available devices')
    args = parser.parse_args()

    port = int(args.port)
    address = args.address
    mouse = args.mouse

    if args.list:
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        for device in devices:
            print(device.path, device.name, device.phys)

    else:
        dev = evdev.InputDevice(f'/dev/input/{mouse}')
        print(dev)
        dev.grab()
        print(dev.capabilities(True))
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        for event in dev.read_loop():
            data = [event.type, event.code, event.value]
            print(data)
            sock.sendto(bytes(f"{json.dumps(data)}\n", "utf-8"), (address, port))

