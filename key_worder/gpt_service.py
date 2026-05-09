import base64
import json
import sys
from pathlib import Path

from openai import OpenAI

client = OpenAI(api_key="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")


def _prompt_file_candidates() -> list[Path]:
    if getattr(sys, "frozen", False):
        return [Path(sys.executable).resolve().parent / "prompt.txt"]
    return [Path(__file__).resolve().parent / "prompt.txt"]


def load_prompt() -> str:
    for path in _prompt_file_candidates():
        if path.is_file():
            return path.read_text(encoding="utf-8")
    tried = ", ".join(str(p) for p in _prompt_file_candidates())
    raise FileNotFoundError(f"prompt.txt not found. Tried: {tried}")


def send_photo_to_openai(image_path: str):
    prompt = load_prompt()

    with open(image_path, "rb") as f:
        image_bytes = f.read()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[{
            "role": "user",
            "content": [
                {"type": "input_text", "text": prompt},
                {
                    "type": "input_image",
                    "image_url": f"data:image/jpeg;base64,{image_base64}"
                }
            ]
        }]
    )

    answer = response.output_text.replace('```json', '').replace('```', '')

    parsed = json.loads(answer)

    return parsed
