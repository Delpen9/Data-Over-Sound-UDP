from scipy.io import wavfile
from scipy.signal import find_peaks
import numpy as np

def collect_data(directory):
    fs, data = wavfile.read(directory)
    data = [np.int64(i) for i in data]
    return data

# TODO: Replace with start and end frequencies of carrier length 10
def find_edges(data):
    max_value = np.amax(data)
    data = [i if i > 1/10*max_value else 0 for i in data]
    peaks, _ = find_peaks(data, None, 0, 1, 1)    ## Look into this. It might detect incorrect peaks. Potential to break the whole program
    left_edge = peaks[0]
    right_edge = peaks[len(peaks) - 1]
    return left_edge, right_edge

def accumulate_frequency_samples(left_position, right_position, data):
    frequency_samples = []
    for i in range(data[left_position], data[right_position] + 1):
        if data[i] > 0 and data[i - 1] < 0:
            frequency_samples.append(i)
        elif data[i] < 0 and data[i - 1] > 0:
            frequency_samples.append(i)
    return frequency_samples

def find_carrier_frequency(frequency_samples):
    consecutive_values = np.absolute(np.array(frequency_samples[1:]) - np.array(frequency_samples[:-1]))
    consecutive_values = [i if i < 4 else 1 for i in consecutive_values]
    frequency_mean = np.mean(consecutive_values, 0)
    frequency = 44100/(2*frequency_mean)
    return frequency

def match_carrier(frequency):
    for carrier in range(10800, 12600, 200):
        if np.abs(frequency - carrier) <= 100:
            return carrier
    return None

def samples_to_carrier(left_position, right_position, data):
    frequency_samples = accumulate_frequency_samples(left_position, right_position, data)
    frequency = find_carrier_frequency(frequency_samples)
    carrier = match_carrier(frequency)
    return carrier

# By the 'sliding door' method, move from left to right at
# increments of 441 bits, using frequency demodulation from the
# bands between 10800 - 12600 bits, inclusive, at increments of
# 200 bits. This totals to be about 10 different frequencies. 
# At a baud rate of 100 bps, this means that the effective bps is 
# 300 bps with a start and end frequency. 
# By implementing Amplitude modulation, you can get a 
# multiplier effect of x2 for two distinguishable, 
# non-zero amplitudes to then be 400 bps.
# Using an amplitude of 0 will only result in a carrier increase of 1,
# contributing to the additive effect. However, this may jeopardize the
# quality of the algorithm for litte gain.
def sliding_door(left_edge, right_edge, data):
    carrier_list = []
    for bit in range(left_edge, right_edge + 1, 441):
        carrier = samples_to_carrier(bit, bit + 441, data)
        carrier_list.append(carrier)
    return carrier_list