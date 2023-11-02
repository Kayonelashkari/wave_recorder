import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import wave

# Initialize PyAudio
p = pyaudio.PyAudio()

# Set audio stream parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 96000  # Set the sample rate to 96 kHz
CHUNK = 2048

# Initialize the audio stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

# Initialize Matplotlib plot
plt.ion()
fig, ax = plt.subplots()

# Create a .wav file to save the recorded audio
output_filename = "recorded_audio.wav"
output_file = wave.open(output_filename, 'wb')
output_file.setnchannels(CHANNELS)
output_file.setsampwidth(p.get_sample_size(FORMAT))
output_file.setframerate(RATE)

try:
    # Loop to continuously get data
    while True:
        # Read audio stream and handle overflow
        try:
            audio_data = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
        except IOError:
            continue  # Skip this iteration due to overflow

        # Save audio data to the .wav file
        output_file.writeframes(audio_data.tobytes())

        # Calculate FFT and update the plot
        Pxx, freqs, bins, im = ax.specgram(audio_data, NFFT=1024, Fs=RATE, noverlap=512, scale='dB')
        plt.pause(0.001)
        ax.clear()

except KeyboardInterrupt:
    # Stop and close the audio stream and plot
    stream.stop_stream()
    stream.close()
    p.terminate()
    plt.close('all')

    # Close and save the .wav file
    output_file.close()
