#!/usr/bin/python3

import argparse
import evdev
import socket
import json
import asyncio

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


async def handle_events(device):
    async for event in device.async_read_loop():
        if event.code == 127:
            device.ungrab()
            exit()

        data = [event.type, event.code, event.value]
        sock.sendto(bytes(f"{json.dumps(data)}\n", "utf-8"), (address, port))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Keyboard and Mouse Event listener')
    parser.add_argument('--address', '-a', type=str, help='address to connect to', default='localhost')
    parser.add_argument('--port', '-p', type=str, help='port to connect to', default=4545)
    parser.add_argument('--mouse', '-m', type=str, help='mouse event', default='event7')
    parser.add_argument('--keyboard', '-k', type=str, help='keyboard event', default='event2')
    parser.add_argument('--list', '-l', help='list available devices')
    args = parser.parse_args()

    port = int(args.port)
    address = args.address
    mouse_input = args.mouse
    keyboard_input = args.keyboard

    if args.list:
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        for dev in devices:
            print(dev.path, dev.name, dev.phys)
    else:
        mouse = evdev.InputDevice(f'/dev/input/{mouse_input}')
        mouse.grab()
        keyboard = evdev.InputDevice(f'/dev/input/{keyboard_input}')
        keyboard.grab()

        for device in mouse, keyboard:
            asyncio.ensure_future(handle_events(device))

        loop = asyncio.get_event_loop()
        loop.run_forever()
