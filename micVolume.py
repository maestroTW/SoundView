import sounddevice as sd
import numpy as np

current_volume = None


def print_sound(indata, outdata, frames, time, status):
    global current_volume
    volume_norm = int(np.linalg.norm(indata) * 10)
    current_volume = volume_norm
    print(current_volume)


with sd.Stream(callback=print_sound):
    sd.sleep(-1)
