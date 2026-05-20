import os
from dotenv import load_dotenv
from llama_cpp import Llama

load_dotenv()
load_dotenv(dotenv_path="./src/.env.public")

MODEL_NAME = os.getenv("TEXT_GENERATOR_FILE_NAME")
MODEL_PATH = f"./models/{MODEL_NAME}"
SYSTEM_CONTENT = os.getenv("TEXT_GENERATOR_SYSTEM_CONTENT")

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=8096,
)

system_msg = {"role": "system", "content": SYSTEM_CONTENT}
messages = [system_msg]

def getAiResponse(user_input: str):
    messages.append({"role": "user", "content": user_input})

    response = llm.create_chat_completion(
        messages=messages,
        temperature=0.7,
        top_p=0.9,
        max_tokens=1024 * 8,
    )

    assistant_reply = response['choices'][0]['message']['content']
    messages.append({"role": "assistant", "content": assistant_reply})

    return assistant_reply

def clearAiMessages():
    global messages
    messages = [system_msg]
