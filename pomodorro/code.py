# pyright: reportShadowedImports=false, reportMissingImports=false
import math

import board
import digitalio
import neopixel
from adafruit_debouncer import Button
from alarm import Alarm
from timer import Timer

MINUTES_25 = 60 * 25
MINUTES_5 = 60 * 5
RED = (255, 0, 0)
GREEN = (0, 255, 0)
OFF = (0, 0, 0)

button_a = digitalio.DigitalInOut(board.BUTTON_A)
button_a.switch_to_input(digitalio.Pull.DOWN)
pixels = neopixel.NeoPixel(board.NEOPIXEL, n=10, auto_write=False, brightness=0.3)


def wait_for_press(button: Button):
    button.update()
    button.update()
    while not button.pressed:
        button.update()


def main():
    pomo_alarm = Alarm("beep.wav")
    continue_button = Button(button_a)
    pomo_timer = Timer()
    focus_time = True
    while True:
        wait_for_press(continue_button)

        pomo_timer.duration = MINUTES_25 if focus_time else MINUTES_5
        pixel_color = RED if focus_time else GREEN
        pixels.fill(pixel_color)
        pixels.show()
        pomo_timer.start()

        while not pomo_timer.is_expired:
            n_on = max(pomo_timer.remaining / pomo_timer.duration * pixels.n, 0.0)
            remainder, whole = math.modf(pixels.n - n_on)
            n_off = int(whole)
            pixels[:n_off] = [OFF] * n_off
            if n_off < pixels.n:
                pixels[n_off] = tuple(x * (1 - remainder) for x in pixel_color)
            pixels.show()
        pixels.fill(OFF)
        pixels.show()

        pomo_alarm.start()
        wait_for_press(continue_button)
        pomo_alarm.stop()

        focus_time = not focus_time


main()
