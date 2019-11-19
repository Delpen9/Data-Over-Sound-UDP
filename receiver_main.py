import threading
import Queue
import time
import pyaudio
import wave
import demodulate

q = Queue()
# TODO: Make this accumulate over time - recording history
directory = 'audio_bin/wav_' + str(1) + '.wav'

class producer_thread(threading.Thread):
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 100
    def run(self):
        # Startup pyaudio instance
        audio = pyaudio.PyAudio()

        # start Recording
        stream = audio.open(
            format = FORMAT,
            channels = CHANNELS,
            rate=RATE,
            input = True,
            frames_per_buffer = CHUNK
        )

        frames = []
        packet = []

        # Record
        # TODO: Possibility that what is inside this while loop is too slow
        send_interval = int(RATE / CHUNK)
        time = 1
        while self.running:
            time += 1
            data = stream.read(CHUNK)
            packet.append(data)
            frames.append(data) # This data is never deleted
            if (time % send_interval == 0):
                q.put(packet)
                packet = []

        # Stop Recording
        stream.stop_stream()
        stream.close()
        audio.terminate()

        # Write your new .wav file
        waveFile = wave.open(directory, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()

        q.put(None) # Termination Code

class consumer_thread(Thread):
    def run(self):
        data = []
        while True:
            datum = q.get()

            if datum is None:
                return data
            data.extend(datum)

            if is_packet_end(datum):
                return data

## --------------------------------------------------------
## Write a DSP Algorithm to determine if packets ends
## --------------------------------------------------------
def is_packet_end(data):
    # ------------
    # algorithm goes here
    # ------------
    return False
## --------------------------------------------------------
## /Finished
## --------------------------------------------------------

def receiver_instance(directory):
    receive.record_audio(directory)

if __name__ == '__main__':
    # Create Producer
    p = producer_thread(name = 'producer')
    # Create Consumer
    c = consumer_thread(name = 'consumer')

    p.start()
    c.start()

    # TODO: Get this to trigger at the correct time
    p.running = False
    p.join()
    c.join()

    data = demodulate.collect_data(directory)
    left_edge, right_edge = demodulate.find_edges(data)

    # -----------------------------------------------------
    # Code to do something with the demodulated information
    # -----------------------------------------------------

    print('Recording Ended')
