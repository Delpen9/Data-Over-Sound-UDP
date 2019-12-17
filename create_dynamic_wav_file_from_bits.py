import numpy as np
from scipy.io import wavfile
import pyaudio
import sox
import os

sampleRate = 88200
duration = 0.005
move_ahead = duration/(sampleRate * duration)

frequency = 10600

t = np.linspace(0, duration, sampleRate * duration)
y = 0*np.sin(frequency * 2 * np.pi * t)

for i in range(1, 11):
  t = np.linspace(duration + move_ahead, 2 * duration, sampleRate * duration)
  y = np.append(y, 10*np.sin(frequency * 2 * np.pi * t))
        
for i in range(11, 290):
  frequency = 10600 + 200*(np.abs(10 - i) % 10)
  t = np.linspace(duration + move_ahead, 2 * duration, sampleRate * duration)
  y = np.append(y, 10*np.sin(frequency * 2 * np.pi * t))

frequency = 12600
for i in range(290, 300):
  t = np.linspace(duration + move_ahead, 2 * duration, sampleRate * duration)
  y = np.append(y, 10*np.sin(frequency * 2 * np.pi * t))

wavfile.write('Sine.wav', sampleRate, y)

os.system('sox Sine.wav -e signed-integer -r 88200 -c 1 -b 16 Better_Sine.wav')
