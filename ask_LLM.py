import json
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import os

# Charger la clé API
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Charger les produits
with open("produits_dict.json", "r", encoding="utf-8") as f:
    produits = json.load(f)

# Fonction pour générer uniquement la description
def generer_description(produit):
    caracs = ", ".join(
        [f"{cle.capitalize()} : {val}" for cle, val in produit.get("caracteristiques", {}).items() if val]
    )

    prompt = f"""
    Rédige une description marketing (3 phrases maximum) pour ce produit.

    Nom : {produit.get('nom')}
    Marque : {produit.get('marque')}
    Catégorie : {produit.get('categorie')}
    Prix : {produit.get('prix')} €
    Caractéristiques : {caracs}
    """


    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def generer_prompt_image(description_produit):
    """
    Génère un prompt visuel pour l'image à partir de la description marketing.
    """
    prompt = f"""
    À partir de la description suivante d’un produit :
    {description_produit}

    Génère un prompt court (en anglais) décrivant une image réaliste de ce produit.
    Exemple : "realistic product photo of a white Nike sneaker size 42 on a neutral background"
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()


import base64
from io import BytesIO
from PIL import Image

def generer_image(prompt_image, taille="1024x1024"):
    response = client.images.generate(
        model="gpt-image-1",
        prompt=prompt_image,
        size=taille
    )

    # Vérifier si c'est une URL ou du base64
    if hasattr(response.data[0], "url") and response.data[0].url:
        return response.data[0].url
    elif hasattr(response.data[0], "b64_json") and response.data[0].b64_json:
        image_data = base64.b64decode(response.data[0].b64_json)
        return Image.open(BytesIO(image_data))  # retourne une image PIL
    else:
        return None



