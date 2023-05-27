#!/usr/bin/python3

import argparse
import socketserver
import json

from evdev import UInput, ecodes as e, InputDevice

"""
    ('EV_SYN', 0): [('SYN_REPORT', 0), ('SYN_CONFIG', 1), ('SYN_MT_REPORT', 2), ('?', 4), ('?', 21)],
    ('EV_KEY', 1): [
        (['BTN_LEFT', 'BTN_MOUSE'], 272), ('BTN_RIGHT', 273), ('BTN_MIDDLE', 274), ('BTN_SIDE', 275),
        ('BTN_EXTRA', 276), ('BTN_FORWARD', 277), ('BTN_BACK', 278), ('BTN_TASK', 279), ('?', 280),
        ('?', 281), ('?', 282), ('?', 283), ('?', 284), ('?', 285), ('?', 286), ('?', 287)],
    ('EV_REL', 2): [('REL_X', 0), ('REL_Y', 1), ('REL_HWHEEL', 6), ('REL_WHEEL', 8), ('REL_WHEEL_HI_RES', 11), ('REL_HWHEEL_HI_RES', 12)],
    ('EV_MSC', 4): [('MSC_SCAN', 4)]
"""

cap = {
    e.EV_KEY: [272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287],
    e.EV_REL: [0, 1, 6, 8, 11, 12],
    e.EV_MSC: [4]
}


class EventServer(socketserver.BaseRequestHandler):

    ui = UInput(cap, name='example-device', version=0x3)

    def handle(self):
        data = self.request[0].strip()
        j_data = json.loads(data)

        self.ui.write(j_data[0], j_data[1], j_data[2])
        self.ui.syn()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Network Keyboard and Mouse Switch')
    parser.add_argument('--address', '-a', type=str, help='port to listen on', default='localhost')
    parser.add_argument('--port', '-p', type=str, help='port to listen on', default=4545)

    args = parser.parse_args()

    port = int(args.port)
    address = args.address

    with socketserver.UDPServer((address, port), EventServer) as server:
        server.serve_forever()
