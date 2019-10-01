from scipy.io import wavfile
from scipy.signal import find_peaks, peak_widths
from teager_py import Teager
from math import *
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import pyaudio # Soundcard audio I/O access library
import wave # Python 3 module for reading / writing simple .wav files


# ------------------------------
#TODO: Claps at the front and the back should be processed based on preceding and proceeding .wav files.
# ------------------------------
# # Setup channel info
# FORMAT = pyaudio.paInt16 # data type format
# CHANNELS = 1 # Adjust to your number of channels
# RATE = 44100 # Sample Rate
# CHUNK = 44100 # Block Size
# RECORD_SECONDS = 5 # Record time
# WAVE_OUTPUT_FILENAME = "file17.wav"

# # Startup pyaudio instance
# audio = pyaudio.PyAudio()

# # start Recording
# stream = audio.open(format=FORMAT, channels=CHANNELS,
#                 rate=RATE, input=True,
#                 frames_per_buffer=CHUNK)
# print ("recording...")

# frames = []

# # Record for RECORD_SECONDS
# for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#     data = stream.read(CHUNK)
#     frames.append(data)
# print ("finished recording")

# # Stop Recording
# stream.stop_stream()
# stream.close()
# audio.terminate()

# # Write your new .wav file with built in Python 3 Wave module
# waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
# waveFile.setnchannels(CHANNELS)
# waveFile.setsampwidth(audio.get_sample_size(FORMAT))
# waveFile.setframerate(RATE)
# waveFile.writeframes(b''.join(frames))
# waveFile.close()

fs, data = wavfile.read('file7.wav')

data = [np.int64(i) for i in data]

# Teager
# !IMPORTANT
# Consider reversing the data set then performing the teager operator again
# Compare the results of both to get middle values
teager_first_data = Teager(np.abs(data), 'horizontal', 1)
teager_first_data = [np.int64(i) for i in teager_first_data]

teager_second_data = Teager(np.abs(teager_first_data), 'horizontal', 1)
teager_second_data = [np.int64(i) for i in teager_second_data]

max_value = np.amax(teager_second_data)
# This might need to be improved but does work well currently
post_processed = [i if i > 1/100*max_value else 0 for i in teager_second_data]

# Find Peaks
# !IMPORTANT
# Use this function multiple times to get different bit ranges
# 1000 picks up i % 4 very well while 500 picks up i % 2 very well
# spacing between bits at rate of 100 bits/s is approximately 250: 
# 0 --> 1 = distance of 250

#Height value should modulate depending on quality of the signal
peaks, _ = find_peaks(post_processed, None, 0, 1, 1/27*max_value, [1, 3])
peak_dimensions = peak_widths(post_processed, peaks, rel_height=0.5)

print(peaks)
print(peak_dimensions[0])

chunk_list = []
post_processed_data_chunk = []
for i in range(len(peaks)):
    if len(chunk_list) == 0:
        chunk_list.append(peaks[i])
    ## Distance value should modulate depending on bit spacing
    elif peaks[i] - peaks[i - 1] < 150:
        chunk_list.append(peaks[i])
        if i == len(peaks) - 1:
            post_processed_data_chunk.append(chunk_list)
    else:
        post_processed_data_chunk.append(chunk_list)
        chunk_list = []
        chunk_list.append(peaks[i])
        if i == len(peaks) - 1:
            post_processed_data_chunk.append(chunk_list)

post_processed_data_chunk = [floor(np.mean(i)) for i in post_processed_data_chunk]

print(len(post_processed_data_chunk))

post_processed_data = [1 for i in teager_second_data]
for i in range(len(teager_second_data)):
    if i not in post_processed_data_chunk:
        post_processed_data[i] = 0

# Time for Plots
time = np.arange(1, len(data) + 1)
time_first_teager = np.arange(1, len(teager_first_data) + 1)
time_second_teager = np.arange(1, len(teager_second_data) + 1)
time_post_processed = np.arange(1, len(post_processed) + 1)

# Begin Plotting
gs = gridspec.GridSpec(4,1)
fig = plt.figure()

# First Plot
ax = fig.add_subplot(gs[0])
ax.plot(time, data)
ax.set_ylabel(r'Raw Data', size = 16)
ax.get_yaxis().set_label_coords(-0.1, 0.5)
plt.tick_params(
    axis='x',          # changes apply to the x-axis
    labelbottom=False) # labels along the bottom edge are off

# Second Plot
ax = fig.add_subplot(gs[1])
ax.plot(time_first_teager, teager_first_data)
ax.set_ylabel(r'Teager 1', size = 16)
ax.get_yaxis().set_label_coords(-0.1, 0.5)
plt.tick_params(
    axis='x',          # changes apply to the x-axis
    labelbottom=False) # labels along the bottom edge are off

# Third Plot
ax = fig.add_subplot(gs[2])
ax.plot(time_second_teager, teager_second_data)
ax.set_ylabel(r'Teager 2', size = 16)
ax.get_yaxis().set_label_coords(-0.1, 0.5)
plt.tick_params(
    axis='x',          # changes apply to the x-axis
    labelbottom=False) # labels along the bottom edge are off

# Fourth Plot
ax = fig.add_subplot(gs[3])
ax.plot(time_post_processed, post_processed_data)
ax.set_ylabel(r'Peaks', size = 16)
ax.get_yaxis().set_label_coords(-0.1, 0.5)
plt.tick_params(
    axis='x',          # changes apply to the x-axis
    labelbottom=False) # labels along the bottom edge are off

plt.show()