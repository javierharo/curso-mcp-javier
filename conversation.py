"""In-memory conversation history — the model remembers because we resend it."""

import os
import time
from google.genai import errors
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

MODEL = "gemini-3.6-flash"
SYSTEM_INSTRUCTION = "Eres un asistente breve. Respondes en español."

history: list[dict] = []
MAX_TURNS = 10


def trim_history() -> None:
    """Keep only the most recent conversation turns."""
    max_entries = MAX_TURNS * 2

    if len(history) > max_entries:
        del history[:-max_entries]

def send(message: str, _retries: int = 0) -> str:
    """Send a message while keeping recent conversation history."""

    trim_history()

    history.append(
        {
            "role": "user",
            "parts": [{"text": message}],
        }
    )

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=history,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                thinking_config=types.ThinkingConfig(
                    thinking_level="minimal"
                ),
                max_output_tokens=1000,
            ),
        )

    except errors.ClientError as exc:
        if exc.code == 429 and _retries < 3:
            wait = 2 ** _retries

            print(
                f"[429] Límite de RPM alcanzado. "
                f"Reintentando en {wait}s..."
            )

            time.sleep(wait)

            # Remove the user message before retrying,
            # so it is not duplicated in history.
            history.pop()

            return send(
                message,
                _retries=_retries + 1,
            )

        history.pop()

        return (
            f"Error del cliente ({exc.code}): "
            f"{exc.message}. No se reintenta."
        )

    except errors.ServerError as exc:
        if _retries < 3:
            wait = 2 ** _retries

            print(
                f"[{exc.code}] Error del servidor. "
                f"Reintentando en {wait}s..."
            )

            time.sleep(wait)
            history.pop()

            return send(
                message,
                _retries=_retries + 1,
            )

        history.pop()

        return (
            "El servicio no respondió tras varios "
            f"intentos ({exc.code})."
        )

    usage = response.usage_metadata

    print(
        f"[tokens] TOTAL: "
        f"{usage.total_token_count}"
    )

    finish_reason = str(
        response.candidates[0].finish_reason
    )

    if "MAX_TOKENS" in finish_reason:
        print(
            "[warning] Respuesta truncada "
            "por max_output_tokens."
        )

    history.append(
        {
            "role": "model",
            "parts": [{"text": response.text}],
        }
    )

    return response.text


def main() -> None:
    print(send("Me llamo Alex y mi color favorito es el verde."))
    print(send("¿Qué framework de Python vimos en la Clase 1?"))
    print(send("Dame un ejemplo de dato que no cabe en un int."))
    print(send("¿Qué hace el comando uv init?"))
    print(send("Explica en una frase qué es un token."))
    print(send("¿Qué significa que una API sea stateless?"))
    print(send("¿Para qué sirve un archivo .env?"))
    print(send("¿Cómo me llamo y cuál es mi color favorito?"))


if __name__ == "__main__":
  def main() -> None:
    messages = [
        "Me llamo Alex y mi color favorito es el verde.",
        "¿Qué framework de Python vimos en la Clase 1?",
        "Dame un ejemplo de dato que no cabe en un int.",
        "¿Qué hace el comando uv init?",
        "Explica en una frase qué es un token.",
        "¿Qué significa que una API sea stateless?",
        "¿Para qué sirve un archivo .env?",
        "¿Cómo me llamo y cuál es mi color favorito?",
    ]

    for message in messages:
        print(send(message))
        time.sleep(13)




def trigger_rate_limit() -> None:
    """Send repeated requests to trigger the provider rate limit."""

    history.clear()

    for i in range(1, 21):
        print(
            f"Request {i}: "
            f"{send(f'Cuenta hasta {i}.')}"
        )


if __name__ == "__main__":
    trigger_rate_limit()