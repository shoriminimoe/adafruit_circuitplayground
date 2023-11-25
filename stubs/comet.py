import adafruit_led_animation.color as color
import board
from adafruit_led_animation.animation.comet import Comet
from neopixel import NeoPixel

pixels = NeoPixel(board.NEOPIXEL, 10, brightness=0.3, auto_write=False)

chase = Comet(
    pixels,
    speed=0.1,
    color=color.PURPLE,
    background_color=color.ORANGE,
    tail_length=3,
)
while True:
    chase.animate()
