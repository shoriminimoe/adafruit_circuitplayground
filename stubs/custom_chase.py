import adafruit_led_animation.color as color
from adafruit_circuitplayground.express import cpx as cp
from adafruit_led_animation.animation.customcolorchase import CustomColorChase

cp.pixels.brightness = 0.3
chase = CustomColorChase(
    cp.pixels, speed=0.1, colors=[color.PURPLE, color.GREEN, color.ORANGE]
)
while True:
    chase.reverse = cp.switch
    chase.animate()
