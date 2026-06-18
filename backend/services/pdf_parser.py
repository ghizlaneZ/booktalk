import pdfplumber
import io  # io permet de traiter des bytes en mémoire comme si c'était un fichier sur disque


def extract_text_from_pdf(file_bytes: bytes) -> str:
    # BytesIO transforme les bytes bruts du PDF en un objet "fichier virtuel" que pdfplumber peut lire
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        # Pour chaque page, on extrait le texte ; si une page est une image (scan), extract_text() retourne None → on met ""
        pages = [page.extract_text() or "" for page in pdf.pages]
    # On joint toutes les pages avec un saut de ligne, et strip() supprime les espaces/sauts en début et fin
    return "\n".join(pages).strip()
