# pyright: reportShadowedImports=false, reportMissingImports=false
import math
import time

import board
import digitalio
import neopixel
from adafruit_debouncer import Button
from adafruit_led_animation.animation.blink import Blink
from micropython import const
from user_alarm import Alarm
from user_timer import Pomodoro

SEC_TO_NS = const(1_000_000_000)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
OFF = (0, 0, 0)

button_a = digitalio.DigitalInOut(board.BUTTON_A)
button_a.switch_to_input(digitalio.Pull.DOWN)
pixels = neopixel.NeoPixel(board.NEOPIXEL, n=10, auto_write=False, brightness=0.3)
led = digitalio.DigitalInOut(board.LED)
led.switch_to_output(value=False)


class LEDBlink:
    def __init__(self, led, period=1):
        self._led = led
        self._period = int(period / 2 * SEC_TO_NS)
        self._next_update = time.monotonic_ns() + self._period

    def animate(self):
        now = time.monotonic_ns()
        if now > self._next_update:
            self._led.value = not self._led.value
            self._next_update = now + self._period


def wait_for_press(button: Button, led_animation=None):
    button.update()
    button.update()
    while not button.pressed:
        if led_animation is not None:
            led_animation.animate()
        button.update()


def main():
    pomo = Pomodoro()
    pomo_alarm = Alarm("beep.wav")
    continue_button = Button(button_a)
    blink = Blink(pixels, speed=0.5, color=YELLOW)
    red_led = LEDBlink(led, period=2)
    while True:
        wait_for_press(continue_button, red_led)
        led.value = False

        pixel_color = RED if pomo.focus_time else GREEN
        pixels.fill(pixel_color)
        pixels.show()
        pomo.start()

        while not pomo.is_expired:
            off_portion = max((1.0 - pomo.remaining / pomo.duration) * pixels.n, 0.0)
            remainder, whole = math.modf(off_portion)
            n_off = int(whole)
            pixels[:n_off] = [OFF] * n_off
            if n_off < pixels.n:
                pixels[n_off] = tuple(x * (1 - remainder) for x in pixel_color)
            pixels.show()
            continue_button.update()
            if continue_button.pressed:
                pomo.pause()
                wait_for_press(continue_button, red_led)
                led.value = False
                pomo.resume()

        pomo_alarm.start()
        wait_for_press(continue_button, blink)
        pomo_alarm.stop()
        pixels.fill(OFF)
        pixels.show()

        pomo.next()


main()
