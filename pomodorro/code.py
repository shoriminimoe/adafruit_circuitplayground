# pyright: reportShadowedImports=false, reportMissingImports=false
import math
import time

import board
import digitalio
import neopixel
from adafruit_debouncer import Button
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
red_led = digitalio.DigitalInOut(board.LED)
red_led.switch_to_output(value=False)


class TimeToggle:
    def __init__(self, period=1):
        self._value = True
        self._period = int(period / 2 * SEC_TO_NS)
        self._next_update = time.monotonic_ns() + self._period

    @property
    def value(self):
        return self._value

    def update(self):
        now = time.monotonic_ns()
        if now > self._next_update:
            self._value = not self._value
            self._next_update = now + self._period


class LEDBlink(TimeToggle):
    def __init__(self, led, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._led = led

    def animate(self):
        self.update()
        self._led.value = self.value


class PixelBlink(TimeToggle):
    def __init__(self, *args, pixels, color, **kwargs):
        super().__init__(*args, **kwargs)
        self._pixels = pixels
        self._color = color

    def animate(self):
        self.update()
        if self.value:
            self._pixels.fill(self._color)
        else:
            self._pixels.fill(OFF)
        self._pixels.show()


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
    blink = PixelBlink(pixels=pixels, period=1, color=YELLOW)
    led_blink = LEDBlink(red_led, period=2)
    while True:
        wait_for_press(continue_button, led_blink)
        red_led.value = False

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
                wait_for_press(continue_button, led_blink)
                red_led.value = False
                pomo.resume()

        pomo_alarm.start()
        wait_for_press(continue_button, blink)
        pomo_alarm.stop()
        pixels.fill(OFF)
        pixels.show()

        pomo.next()


main()
