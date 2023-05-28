#!/usr/bin/python3

import argparse
import evdev
import socket
import json
import asyncio

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address_index = 0
toggle_key_down = False
addresses = []


def get_next_address():
    global address_index
    if address_index == len(addresses)-1:
        address_index = 0
    else:
        address_index = address_index+1


async def handle_events(device):
    global address_index, toggle_key_down
    async for event in device.async_read_loop():
        if event.code == 127:
            if toggle_key_down:
                # Context menu key
                get_next_address()
            toggle_key_down = not toggle_key_down
        elif event.code == 88:
            # F12
            mouse.ungrab()
            keyboard.ungrab()
            exit()
        else:
            data = [event.type, event.code, event.value]
            sock.sendto(bytes(f"{json.dumps(data)}\n", "utf-8"), (addresses[address_index], port))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Keyboard and Mouse Event listener')
    parser.add_argument('--addresses', '-a', type=str, help='addresses to connect to', default='localhost')
    parser.add_argument('--port', '-p', type=str, help='port to connect to', default=4545)
    parser.add_argument('--mouse', '-m', type=str, help='mouse event', default='event7')
    parser.add_argument('--keyboard', '-k', type=str, help='keyboard event', default='event2')
    parser.add_argument('--list', '-l', help='list available devices')
    args = parser.parse_args()

    port = int(args.port)
    addresses = args.addresses.split(",")
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
