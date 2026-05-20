from dotenv import load_dotenv
from faster_whisper import WhisperModel

load_dotenv()

model_size = "base" # "large-v3"
model = WhisperModel(model_size, device="cuda", compute_type="float16")

def getSpeachText(file_path):
        segments, info = model.transcribe(file_path, beam_size=5)
        print("- Detected language '%s' with probability %f" % (info.language, info.language_probability))

        res = ""

        for segment in segments:
            # print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
            res += segment.text + " "

        return res.strip()
