
from evdev import UInput, InputDevice

mouse = InputDevice('/dev/input/event7')


ui = UInput.from_device(mouse, name='keyboard-mouse-device')

print(ui.capabilities(verbose=True).keys())