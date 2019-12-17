import simpleaudio as sa

filename = 'wav_samples/sample_low_var_claps_3.wav'
wave_obj = sa.WaveObject.from_wave_file(filename)
play_obj = wave_obj.play()
play_obj.wait_done()  # Wait until sound has finished playing