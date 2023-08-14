#!/usr/bin/python3

import argparse
import socket
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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Network Keyboard and Mouse Switch')
    parser.add_argument('--server', '-a', type=str, help='NKMS server to connect to', default='localhost')
    parser.add_argument('--port', '-p', type=str, help='port to connect to', default=4777)
    args = parser.parse_args()

    print('Starting NKMS Client ...')
    port = int(args.port)
    server_address = args.server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        sock.connect((server_address, port))

        data = str(sock.recv(50000), "utf-8").strip()
        try:
            new_caps = {}
            dev_caps = json.loads(data)
            for k in dev_caps.keys():
                new_caps[int(k)] = dev_caps[k]
        except json.decoder.JSONDecodeError:
            print('Error: Unable to load device capabilities. Falling back to defaults.')
            new_caps = capabilities

        ui = UInput(new_caps, name='NetKMSwitch Keyboard and Mouse')

        while 1:
            data = str(sock.recv(1024), "utf-8").strip().split("\n")
            for line in data:
                try:
                    j_data = json.loads(line)
                except json.decoder.JSONDecodeError:
                    print('Error: json decode failed')
                    continue

                ui.write(j_data[0], j_data[1], j_data[2])
                ui.syn()


