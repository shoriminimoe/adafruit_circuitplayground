# pyright: reportShadowedImports=false, reportMissingImports=false
import math

import board
import digitalio
import neopixel
from adafruit_debouncer import Button
from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.pulse import Pulse
from user_alarm import Alarm
from user_timer import Pomodoro

RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
OFF = (0, 0, 0)

button_a = digitalio.DigitalInOut(board.BUTTON_A)
button_a.switch_to_input(digitalio.Pull.DOWN)
pixels = neopixel.NeoPixel(board.NEOPIXEL, n=10, auto_write=False, brightness=0.3)


def wait_for_press(button: Button, led_animation=None):
    button.update()
    button.update()
    while not button.pressed:
        if led_animation is not None:
            led_animation.animate()
        button.update()


Pomodoro.focus_duration = 5
Pomodoro.short_break_duration = 1
Pomodoro.long_break_duration = 3


def main():
    pomo = Pomodoro()
    pomo_alarm = Alarm("beep.wav")
    continue_button = Button(button_a)
    blink = Blink(pixels, speed=0.5, color=YELLOW)
    pulse = Pulse(pixels, speed=0.5, color=YELLOW)
    while True:
        wait_for_press(continue_button, pulse)

        pixel_color = RED if pomo.focus_time else GREEN
        pixels.fill(pixel_color)
        pixels.show()
        pomo.start()

        while not pomo.is_expired:
            off_portion = max((1.0 - pomo.remaining / pomo.duration) * pixels.n, 0.0)
            remainder, whole = math.modf(off_portion)
            n_off = int(whole)
            print(f"{off_portion=}, {remainder=}, {whole=}")
            pixels[:n_off] = [OFF] * n_off
            if n_off < pixels.n:
                pixels[n_off] = tuple(x * (1 - remainder) for x in pixel_color)
            pixels.show()

        pomo_alarm.start()
        wait_for_press(continue_button, blink)
        pomo_alarm.stop()
        pixels.fill(OFF)
        pixels.show()

        pomo.next()


main()
