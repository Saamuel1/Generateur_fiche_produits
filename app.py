import streamlit as st
import pandas as pd
import json
from ask_LLM import generer_description, generer_prompt_image, generer_image

# -----------------------
# 3. Interface Streamlit
# -----------------------
st.title("🛒 Générateur de fiches produits avec image")
st.write("Choisissez un produit → description marketing + image générée automatiquement")

uploaded_file = st.file_uploader("Importer un fichier produits (.csv ou .json)", type=["csv", "json"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
        produits = df.to_dict(orient="records")
    else:
        produits = json.load(uploaded_file)
        df = pd.DataFrame(produits)

    st.success(f"{len(produits)} produits chargés")
    noms_produits = [p["Product ID"] for p in produits if "Product ID" in p]
    choix = st.selectbox("🔽 Choisissez un produit", noms_produits)

    if st.button("🚀 Générer la fiche + image"):
        produit = next(p for p in produits if p.get("Product ID") == choix)

        # Étape 1 : Description produit
        description = generer_description(produit)

        # Étape 2 : Prompt image
        prompt_img = generer_prompt_image(description)

        # Étape 3 : Générer l'image
        image_url = generer_image(prompt_img)

        # Affichage
        st.subheader("Résultat")
        st.write(f"**Nom :** {produit.get('Product Name')}")
        st.write(f"**Marque :** {produit.get('Brand')}")
        st.write(f"**Catégorie :** {produit.get('Category')}")
        st.write(f"**Prix :** {produit.get('Price')} €")
        st.write(f"**Description générée :**\n{description}")


        st.image(image_url, caption=produit.get("nom"), use_column_width=True)
