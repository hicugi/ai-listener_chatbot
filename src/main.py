import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from speach_to_text import getSpeachText
from text_generator import getAiResponse

WAV_DIRECTORY_PATH = "./records"

is_wav_processing = False

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
        is_wav_processing = True

        print("- New recording:", file_path)

        speach_input = getSpeachText(file_path)

        print("- Sending the text to AI:", speach_input)
        print("--------------------------------------------")

        output = getAiResponse(speach_input)

        print("--------------------------------------------")
        print(output)

        file_name = file_path[file_path.rfind("/")+1:]
        text_file_path = f"./public/{file_name}.txt"
        with open(text_file_path, "w") as f:
            f.write(output)

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

