# pyright: reportShadowedImports=false
import time

import adafruit_led_animation.color as color
from adafruit_ble import BLERadio
from adafruit_ble.advertising import Advertisement
from adafruit_circuitplayground.bluefruit import cpb
from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.pulse import Pulse


def ble_notifier():
    ble = BLERadio()
    advertisement = Advertisement()
    advertisement.short_name = "Do not disturb indicator"
    advertisement.connectable = True
    cpb.pixels.brightness = 0.3
    blue_comet = Comet(
        cpb.pixels,
        speed=0.1,
        color=color.BLUE,
        tail_length=4,
        bounce=True,
    )
    amber_blink = Blink(cpb.pixels, speed=1, color=color.AMBER)
    red_pulse = Pulse(cpb.pixels, 0.005, color.RED, 2.5)
    while True:
        first_round = True
        ble.start_advertising(advertisement)
        while not ble.connected:
            blue_comet.animate()
        while ble.connected:
            if first_round:
                start = time.monotonic()
                while time.monotonic() - start < 30:
                    amber_blink.animate()
                first_round = False
            red_pulse.animate()


ble_notifier()
