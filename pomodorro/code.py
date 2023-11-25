# pyright: reportShadowedImports=false, reportMissingImports=false
import math

import board
import digitalio
import neopixel
from adafruit_debouncer import Button
from user_alarm import Alarm
from user_timer import Pomodoro

MINUTES_25 = 60 * 25
MINUTES_5 = 60 * 5
RED = (255, 0, 0)
GREEN = (0, 255, 0)
OFF = (0, 0, 0)

button_a = digitalio.DigitalInOut(board.BUTTON_A)
button_a.switch_to_input(digitalio.Pull.DOWN)
pixels = neopixel.NeoPixel(board.NEOPIXEL, n=10, brightness=0.3)


def wait_for_press(button: Button):
    button.update()
    button.update()
    while not button.pressed:
        button.update()


def main():
    pomo = Pomodoro()
    pomo_alarm = Alarm("beep.wav")
    continue_button = Button(button_a)
    while True:
        wait_for_press(continue_button)

        pixel_color = RED if pomo.focus_time else GREEN
        pixels.fill(pixel_color)
        pomo.start()

        while not pomo.is_expired:
            off_portion = min((1.0 - pomo.remaining / pomo.duration) * pixels.n, 1.0)
            remainder, whole = math.modf(off_portion)
            n_off = int(whole)
            pixels[:n_off] = [OFF] * n_off
            if n_off < pixels.n:
                pixels[n_off] = tuple(x * remainder for x in pixel_color)
        pixels.fill(OFF)

        pomo_alarm.start()
        wait_for_press(continue_button)
        pomo_alarm.stop()

        pomo.next()


main()
