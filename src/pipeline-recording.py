import os
import queue
import time
import wave
from datetime import datetime

import numpy as np
import sounddevice as sd

# =========================
# CONFIG
# =========================
DEVICE_ID = 14
CHANNELS = 32
SAMPLE_RATE = 44100

BLOCK_DURATION = 0.5          # seconds
SILENCE_THRESHOLD = 0.04      # lower = more sensitive
MAX_SILENCE_SECONDS = 3

OUTPUT_DIR = "./records"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# =========================
# STATE
# =========================
audio_queue = queue.Queue()

recording = False
current_audio = []
silence_time = 0

def save_wav(frames):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}.wav"

    tmp_file_path = filename
    output_path = os.path.join(OUTPUT_DIR, filename)

    audio = np.concatenate(frames, axis=0)

    with wave.open(tmp_file_path, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)  # int16
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes((audio * 32767).astype(np.int16).tobytes())

    os.rename(tmp_file_path, output_path)
    print(f"Saved: {filename}")


def audio_callback(indata, frames, time_info, status):
    if status:
        print(status)

    audio_queue.put(indata.copy())


print("Listening... Press Ctrl+C to stop.")

block_size = int(SAMPLE_RATE * BLOCK_DURATION)

with sd.InputStream(
    device=DEVICE_ID,
    samplerate=SAMPLE_RATE,
    channels=CHANNELS,
    blocksize=block_size,
    callback=audio_callback,
):
    try:
        while True:
            chunk = audio_queue.get()

            volume = np.max(np.abs(chunk))

            # Voice detected
            if volume > SILENCE_THRESHOLD:
                if not recording:
                    print("Recording started")

                recording = True
                silence_time = 0
                current_audio.append(chunk)

            # Silence
            else:
                if recording:
                    current_audio.append(chunk)
                    silence_time += BLOCK_DURATION

                    # End recording after long silence
                    if silence_time >= MAX_SILENCE_SECONDS:
                        print("Recording stopped")

                        save_wav(current_audio)

                        current_audio = []
                        recording = False
                        silence_time = 0

    except KeyboardInterrupt:
        print("\nStopped.")
