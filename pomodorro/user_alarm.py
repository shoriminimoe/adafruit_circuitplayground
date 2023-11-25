import audiocore
import board
import digitalio

try:
    import audioio

    audio_out = audioio.AudioOut
except ImportError:
    import audiopwmio

    audio_out = audiopwmio.PWMAudioOut


class Alarm:
    def __init__(self, wav_file):
        self._data = open(wav_file, "rb")
        self._wav = audiocore.WaveFile(self._data)
        self._speaker = audio_out(board.SPEAKER)
        self._speaker_enable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
        self._speaker_enable.switch_to_output(value=True)
        self.stop()

    def start(self, loop=True):
        self._speaker_enable.value = True
        self._speaker.play(self._wav, loop=loop)

    def stop(self):
        self._speaker.stop()
        self._speaker_enable.value = False
