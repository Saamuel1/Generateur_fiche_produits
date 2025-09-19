import pandas as pd

# 1. Importer le fichier CSV
# Remplace 'produits.csv' par le chemin de ton fichier Kaggle
df = pd.read_csv("fashion_products.csv")

# 2. Supprimer les colonnes inutiles
# Ici on enlève "User ID" (pas utile pour la fiche produit)
df = df.drop(columns=["User ID"], errors="ignore")

# 3. Renommer les colonnes
df = df.rename(columns={
    "Product ID": "id_produit",
    "Product Name": "nom",
    "Brand": "marque",
    "Category": "categorie",
    "Price": "prix",
    "Rating": "note",
    "Color": "couleur",
    "Size": "taille"
})

# 4. Vérifier les données manquantes
print("Valeurs manquantes :")
print(df.isnull().sum())

# Exemple : supprimer les lignes avec nom ou prix manquant
df = df.dropna(subset=["nom", "prix"])

# 5. Nettoyer les types de données
# Prix → numérique
df["prix"] = pd.to_numeric(df["prix"], errors="coerce")
# Note → numérique
df["note"] = pd.to_numeric(df["note"], errors="coerce")

# 6. (Optionnel) Nettoyer les doublons
df = df.drop_duplicates(subset=["id_produit", "nom"])

# 7. Afficher un aperçu
print(df.head())

# 8. Sauvegarder la version nettoyée
df.to_csv("produits_nettoyes.csv", index=False)
print("✅ Données nettoyées sauvegardées dans produits_nettoyes.csv")

#%%
df_nettoyes = pd.read_csv("produits_nettoyes.csv")

# Fonction qui transforme une ligne en dictionnaire produit
def ligne_en_produit(row):
    return {
        "id": row["id_produit"],
        "nom": row["nom"],
        "marque": row.get("marque", ""),
        "categorie": row.get("categorie", ""),
        "prix": row.get("prix", ""),
        "caracteristiques": {
            "couleur": row.get("couleur", ""),
            "taille": row.get("taille", ""),
            "note": row.get("note", "")
        }
    }

# Appliquer automatiquement à toutes les lignes
produits = df_nettoyes.apply(ligne_en_produit, axis=1).tolist()

# Exemple : afficher les 2 premiers produits
for p in produits[:2]:
    print(p)

# Sauvegarder la liste complète en JSON
import json
with open("produits_dict.json", "w", encoding="utf-8") as f:
    json.dump(produits, f, ensure_ascii=False, indent=4)

print(f"✅ {len(produits)} produits transformés et sauvegardés dans produits_dict.json")

