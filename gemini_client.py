"""Calls Gemini with a system instruction and explicit generation parameters."""

import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

MODEL = "gemini-3.6-flash"
CONTEXT_WINDOW_LIMIT = 1_048_576

SYSTEM_INSTRUCTION = (
    "Eres un instructor de programación para principiantes. "
    "Respondes en español, máximo 3 frases. "
    "Sin jerga sin explicar, sin inventar funciones."
)


def print_budget(contents: list[dict]) -> None:
    """Print the token usage of the current contents."""

    tokens = client.models.count_tokens(
        model=MODEL,
        contents=contents,
    )

    used_ratio = tokens.total_tokens / CONTEXT_WINDOW_LIMIT

    print(
        f"Historial: {tokens.total_tokens} tokens "
        f"({used_ratio:.4%} de la ventana)"
    )


def ask(prompt: str) -> tuple[str, str]:
    """Returns (text, finish_reason)."""

    contents = [
        {
            "role": "user",
            "parts": [{"text": prompt}],
        }
    ]

    print_budget(contents)

    response = client.models.generate_content(
        model=MODEL,
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            thinking_config=types.ThinkingConfig(
                thinking_level="minimal"
            ),
            max_output_tokens=1000,
        ),
    )

    usage = response.usage_metadata

    print(f"prompt    : {usage.prompt_token_count}")
    print(f"respuesta : {usage.candidates_token_count}")
    print(f"TOTAL     : {usage.total_token_count}")

    finish_reason = str(response.candidates[0].finish_reason)

    print(f"finish    : {finish_reason}")

    if "MAX_TOKENS" in finish_reason:
        print(
            "[warning] La respuesta viene truncada "
            "por max_output_tokens."
        )

    return response.text, finish_reason


def main() -> None:
    text, _ = ask("¿Qué opinas de var en JS?")
    print(text)


if __name__ == "__main__":
   def main() -> None:
    first_text, _ = ask("Hola, me llamo Javier.")
    print("BOT:", first_text)

    second_text, _ = ask("¿Cómo me llamo?")
    print("BOT:", second_text)


if __name__ == "__main__":
    main()