import numpy as np
import wave
import os

SAMPLE_RATE = 44100

def generate_tone(filename, frequency=440, duration=0.2):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    tone = 0.5 * np.sin(2 * np.pi * frequency * t)

    audio = (tone * 32767).astype(np.int16)

    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.writeframes(audio.tobytes())


os.makedirs("assets/sounds", exist_ok=True)

generate_tone("assets/sounds/wall_hit.wav", frequency=300)
generate_tone("assets/sounds/paddle_hit.wav", frequency=500)
generate_tone("assets/sounds/brick_hit.wav", frequency=600)
generate_tone("assets/sounds/brick_destroyed.wav", frequency=800)
generate_tone("assets/sounds/life_lost.wav", frequency=200, duration=0.5)

print("All sound files generated successfully.")