#!/usr/bin/python3

import argparse
import evdev
import socket
import json
import asyncio


class nkms_input:
    def __init__(self, args):
        self.args = args
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.address_index = 0

        self.port = int(self.args.port)
        self.addresses = self.args.addresses.split(",")
        self.mouse_input = self.args.mouse
        self.keyboard_input = self.args.keyboard

    def get_next_address(self):
        if self.address_index == len(self.addresses)-1:
            return 0
        return self.address_index+1

    async def handle_events(self, device):
        async for event in device.async_read_loop():
            print(event.code)
            if event.code == 127:
                # Context menu key
                self.address_index = self.get_next_address()
            elif event.code == 88:
                # F12
                device.ungrab()
                exit()
            else:
                data = [event.type, event.code, event.value]
                self.sock.sendto(bytes(f"{json.dumps(data)}\n", "utf-8"), (self.addresses[self.address_index], self.port))

    def begin(self):
        mouse = evdev.InputDevice(f'/dev/input/{self.mouse_input}')
        mouse.grab()
        keyboard = evdev.InputDevice(f'/dev/input/{self.keyboard_input}')
        keyboard.grab()

        for device in mouse, keyboard:
            asyncio.ensure_future(self.handle_events(device))

        loop = asyncio.get_event_loop()
        loop.run_forever()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Keyboard and Mouse Event listener')
    parser.add_argument('--addresses', '-a', type=str, help='addresses to connect to', default='localhost')
    parser.add_argument('--port', '-p', type=str, help='port to connect to', default=4545)
    parser.add_argument('--mouse', '-m', type=str, help='mouse event', default='event7')
    parser.add_argument('--keyboard', '-k', type=str, help='keyboard event', default='event2')
    parser.add_argument('--list', '-l', help='list available devices')
    args = parser.parse_args()

    if args.list:
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        for dev in devices:
            print(dev.path, dev.name, dev.phys)
    else:
        n = nkms_input(args)
        n.begin()
