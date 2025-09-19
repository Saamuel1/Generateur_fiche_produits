import pandas as pd
import json

df = pd.read_csv("fashion_products.csv")

main_columns = {"product id","product name", "brand", "category", "price"}

def row_to_product(row):
    product = {}
    characteristics = {}

    for col, val in row.items():
        if pd.notna(val):  # ignore NaN/empty
            if col.lower() in main_columns:
                product[col] = val
            else:
                characteristics[col] = val

    product["characteristics"] = characteristics
    return product

products = df.apply(row_to_product, axis=1).tolist()

with open("products_dict.json", "w", encoding="utf-8") as f:
    json.dump(products, f, ensure_ascii=False, indent=4)

