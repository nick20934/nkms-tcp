#!/usr/bin/python3

from evdev import UInput, InputDevice

mouse = InputDevice('/dev/input/event2')


ui = UInput.from_device(mouse, name='keyboard-mouse-device', version=0x3)

print(ui.capabilities())