import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from faster_whisper import WhisperModel
from llama_cpp import Llama
import pyautogui

MODEL_PATH = "./models/gemma-4-E4B-it-OBLITERATED-Q4_K_M.gguf"
WAV_DIRECTORY_PATH = "./records"
SYSTEM_CONTENT = "You are a stream viewer. Skip retorical questions"

model_size = "base" # "large-v3"
model = WhisperModel(model_size, device="cuda", compute_type="float16")

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=8096,
)

messages = [
    {"role": "system", "content": SYSTEM_CONTENT},
]

def chat(user_input: str):
    messages.append({"role": "user", "content": user_input})

    response = llm.create_chat_completion(
        messages=messages,
        temperature=0.7,
        top_p=0.9,
        max_tokens=2048,
    )

    assistant_reply = response['choices'][0]['message']['content']
    messages.append({"role": "assistant", "content": assistant_reply})

    return assistant_reply

is_wav_processing = False

class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        global is_wav_processing

        if event.is_directory:
            return

        file_path = event.src_path

        print("============================================")
        print("New file:", file_path)

        if ".wav" not in file_path:
            return
        if is_wav_processing == True:
            return
        is_wav_processing = True

        print("- New recording:", file_path)

        segments, info = model.transcribe(file_path, beam_size=5)
        print("- Detected language '%s' with probability %f" % (info.language, info.language_probability))

        speach_input = ""

        for segment in segments:
            # print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
            speach_input += segment.text + " "

        print("- Sending the text to AI:", speach_input)
        print("--------------------------------------------")

        output = chat(speach_input)

        print("--------------------------------------------")
        print(output)

        pyautogui.write(output, interval=0.1)
        pyautogui.press('enter')

        is_wav_processing = False


if __name__ == "__main__":
    path = WAV_DIRECTORY_PATH # directory to watch

    event_handler = NewFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)

    observer.start()

    print("============================================")
    print(f"Start watching the directory: {path}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

