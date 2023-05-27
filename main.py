import argparse
import uinput

import socketserver
import json


class EventServer(socketserver.BaseRequestHandler):

    EVENTS = (uinput.REL_X, uinput.REL_Y, uinput.BTN_LEFT, uinput.BTN_RIGHT)
    DEVICE = uinput.Device(EVENTS)

    def handle(self):
        data = self.request[0].strip()
        j_data = json.loads(data)
        if j_data["T"] == "M":
            x_y = uinput.REL_X
            if j_data["D"] == "Y":
                x_y = uinput.REL_Y
            print(j_data["D"])
            print(j_data["V"])
            self.DEVICE.emit(x_y, int(j_data["V"]))

        """
        def move_mouse(self, x, y):
        self.DEVICE.emit(uinput.REL_X, x, syn=False)
        self.DEVICE.emit(uinput.REL_Y, y)
        self.DEVICE.syn()
        """


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Network Keyboard and Mouse Switch')
    parser.add_argument('--address', '-a', type=str, help='port to listen on', default='localhost')
    parser.add_argument('--port', '-p', type=str, help='port to listen on', default=4545)

    args = parser.parse_args()

    port = int(args.port)
    address = args.address

    with socketserver.UDPServer((address, port), EventServer) as server:
        server.serve_forever()
