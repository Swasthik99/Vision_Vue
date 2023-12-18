import sounddevice as sd
import soundfile as sf
import os

def record_and_save_alphabet(output_folder, alphabet, input_device):
    os.makedirs(output_folder, exist_ok=True)

    for letter in alphabet:
        input(f"Press Enter and pronounce '{letter}'...")
        filename = os.path.join(output_folder, f"{letter}.wav")
        record_and_save(filename, input_device=input_device)
        play_audio(filename)

def record_and_save(filename, duration=2, sample_rate=48000, dtype="int16", channels=2, gain=1.0, input_device=None):
    print(f"Recording {filename}...")
    recording = sd.rec(int(sample_rate * duration), samplerate=sample_rate, channels=channels, dtype=dtype, device=input_device)
    sd.wait()

    # Adjust gain
    recording = (recording * gain).astype(dtype)

    sf.write(filename, recording, sample_rate, subtype='PCM_24')

def play_audio(filename):
    print(f"Playing {filename}...")
    audio, sample_rate = sf.read(filename, dtype='int16')
    sd.play(audio, samplerate=sample_rate)
    sd.wait()

if __name__ == "__main__":
    output_folder = "alphabet_recordings"
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    # Specify the input device (use the index that corresponds to your microphone)
    input_device = 1  # Adjust this based on your system configuration

    record_and_save_alphabet(output_folder, alphabet, input_device)

    print("Recording and playback complete.")
