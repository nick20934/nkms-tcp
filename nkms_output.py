#!/usr/bin/python3

import argparse
import socketserver
import json

from evdev import UInput, ecodes as e

capabilities = {
    e.EV_KEY: [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
        31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58,
        59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 85, 86, 87,
        88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 113, 114,
        115, 116, 117, 119, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138,
        140, 142, 150, 152, 158, 159, 161, 163, 164, 165, 166, 173, 176, 177, 178, 179, 180, 183, 184, 185, 186, 187,
        188, 189, 190, 191, 192, 193, 194, 240, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287],
    e.EV_REL: [0, 1, 6, 8, 11, 12],
    e.EV_MSC: [4],
    17: [0, 1, 2, 3, 4]
}


class EventServer(socketserver.BaseRequestHandler):

    ui = UInput(capabilities, name='NetKMSwitch Keyboard and Mouse')

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
