from scipy.io import wavfile
from scipy.signal import find_peaks
import numpy as np

def collect_data(directory):
    fs, data = wavfile.read(directory)
    data = [np.int64(i) for i in data]
    return data

# -----------------------------------------------------------------
# TODO: Find start and end frequencies to position packet for demodulation
# -----------------------------------------------------------------
def demodulate_packet(data):
    start_of_packet, end_of_packet = find_packet_boundaries(data)
    carrier_list = sliding_door(start_of_packet, end_of_packet, data)
    return carrier_list

def find_packet_boundaries(data):
    # This is the hard part
    return None

def start_of_packet(carrier_list):
    # This is the hard part
    return None

def end_of_packet(carrier_list):
    # This is the hard part
    return None
# -----------------------------------------------------------------

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

def sliding_door(left_edge, right_edge, data):
    carrier_list = []
    for bit in range(left_edge, right_edge + 1, 441):
        carrier = samples_to_carrier(bit, bit + 441, data)
        carrier_list.append(carrier)
    return carrier_list
