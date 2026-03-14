from pathlib import Path
import sys
import ollama # AI


def generate(prompt: str, model: str = "llama3.2") -> str:
    response = ollama.generate(
        model=model,
        prompt=prompt,
        stream=False,
    )
    return response["response"]

# TODO: REMOVE, only for testing to see if it works:
if __name__ == "__main__":
    print(generate("What is the best way to learn Python?"))