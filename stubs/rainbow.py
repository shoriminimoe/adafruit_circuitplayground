from time import sleep

from adafruit_circuitplayground.express import cpx as cp
from adafruit_led_animation.animation.rainbowcomet import RainbowComet

TONES = (262, 294, 330, 349, 392, 440, 494, 523)
NUM_TONES = len(TONES)

cp.pixels.brightness = 0.3
comet = RainbowComet(cp.pixels, speed=0.1, tail_length=7)
tone_index = 0
playing = False
while True:
    comet.reverse = cp.switch
    comet.animate()

    if cp.button_a and not playing:
        tone_index = (tone_index + 1) % NUM_TONES
    if cp.button_b and not playing:
        tone_index = (tone_index - 1) % NUM_TONES

    if cp.button_a or cp.button_b:
        cp.start_tone(TONES[tone_index])
        playing = True
        sleep(0.05)
    else:
        cp.stop_tone()
        playing = False
