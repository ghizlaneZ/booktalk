import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def ask_question(book_content: str, question: str) -> str:
    prompt = f"""Tu es un assistant qui aide à comprendre des livres.

Voici le contenu du livre :
{book_content}

Question de l'utilisateur : {question}

Réponds de façon claire et concise en français."""

    message = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text


import httpx

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    http_client=httpx.Client(verify=False)
)