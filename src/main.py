import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from speach_to_text import getSpeachText
from text_generator import getAiResponse, clearAiMessages
import threading
from pipeline_recording import startListening, disabledListening, enableListening

WAV_DIRECTORY_PATH = "./records"

is_wav_processing = False

def aiThinking():
    global is_wav_processing
    is_wav_processing = True

    disabledListening()

def aiStopThinking():
    global is_wav_processing
    is_wav_processing = False

    enableListening()


class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        global is_wav_processing

        if event.is_directory:
            return

        file_path = event.src_path

        print("============================================")
        print("- New file:", file_path)

        if ".wav" not in file_path:
            return
        if is_wav_processing == True:
            return
        aiThinking()

        print("- New recording:", file_path)

        speach_input = getSpeachText(file_path)
        print("- Speach to text:", speach_input)

        if "... ..." in speach_input:
            print("- Silence identified, skipping the input")
            aiStopThinking()
            return

        if "skip, skip" in speach_input:
            print("- Skip command identified")
            print("--------------------------------------------")
            aiStopThinking()
            return

        if "Command" in speach_input and "forget everything" in speach_input:
            print("- Clear command identified")
            print("--------------------------------------------")
            clearAiMessages()
            aiStopThinking()
            return

        print("- Sending the text to AI")
        print("--------------------------------------------")

        output = getAiResponse(speach_input)

        print("--------------------------------------------")
        print(output)

        file_name = file_path[file_path.rfind("/")+1:]
        text_file_path = f"./public/{file_name}.txt"
        with open(text_file_path, "w") as f:
            f.write(output)

        aiStopThinking()

def runDirectoryObserver():
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

if __name__ == "__main__":
    threading.Thread(
        target=startListening,
        daemon=True
    ).start()

    threading.Thread(
        target=runDirectoryObserver,
        daemon=True
    ).start()

while True:
    time.sleep(10)
