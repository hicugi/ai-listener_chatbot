from dotenv import load_dotenv
from llama_cpp import Llama

load_dotenv()

MODEL_PATH = "./models/supergemma4-26b-uncensored-fast-v2-Q4_K_M.gguf"
SYSTEM_CONTENT = "You are a stream viewer. Don't extrapolate. Response casual and simple terms."

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=8096,
)

messages = [
    {"role": "system", "content": SYSTEM_CONTENT},
]

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
