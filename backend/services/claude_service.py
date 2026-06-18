import os
import anthropic
import httpx
# load_dotenv lit le fichier .env et injecte les variables dans os.environ
from dotenv import load_dotenv

load_dotenv()

# On crée un client HTTP qui désactive la vérification SSL (verify=False)
# Utile en dev local si tu as des problèmes de certificat, à retirer en production
client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY"),  # lit la clé depuis le .env
    http_client=httpx.Client(verify=False)
)

def ask_question(book_content: str, question: str) -> str:
    # On construit le prompt en injectant le texte du livre et la question de l'utilisateur
    prompt = f"""Tu es un assistant qui aide à comprendre des livres.

Voici le contenu du livre :
{book_content}

Question de l'utilisateur : {question}

Réponds de façon claire et concise en français."""

    # messages.create envoie la requête à l'API Claude et attend la réponse
    message = client.messages.create(
        model="claude-haiku-4-5",   # modèle rapide et économique, suffisant pour Q&A
        max_tokens=1024,             # limite la longueur de la réponse (~750 mots max)
        messages=[{"role": "user", "content": prompt}]  # historique de conversation : un seul message ici
    )
    # content est une liste de blocs ; [0].text prend le texte du premier bloc (la réponse)
    return message.content[0].text
