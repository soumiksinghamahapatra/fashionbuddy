"""
build_catalog.py — loads data/catalog.csv into a local Chroma vector
database, so we can later search it by meaning (not just exact keywords).

Run this once (or any time catalog.csv changes) to (re)build the database.
It creates a folder called chroma_db/ next to this file — that's your
"database", saved to disk, completely free and local.
"""

import os
import pandas as pd
import chromadb

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CATALOG_PATH = os.path.join(CURRENT_DIR, "..", "data", "catalog.csv")
DB_PATH = os.path.join(CURRENT_DIR, "chroma_db")


def build_catalog():
    df = pd.read_csv(CATALOG_PATH)

    # PersistentClient saves the database to disk in DB_PATH so it's
    # still there next time you run a script, instead of disappearing
    # when the program ends.
    client = chromadb.PersistentClient(path=DB_PATH)

    # If we've run this before, start fresh so we don't get duplicates
    try:
        client.delete_collection("fashion_catalog")
    except Exception:
        pass

    # Chroma's default embedding model (all-MiniLM-L6-v2) runs locally
    # on your computer — no API key, no cost, no internet needed after
    # the first run (it downloads the small model once).
    collection = client.create_collection("fashion_catalog")

    collection.add(
        ids=[str(i) for i in range(len(df))],
        documents=df["description"].tolist(),
        metadatas=[
            {
                "product_name": row["product_name"],
                "category": row["category"],
                "price": float(row["price"]),
                "link": row["link"],
            }
            for _, row in df.iterrows()
        ],
    )

    print(f"Loaded {len(df)} products into the catalog at {DB_PATH}")


if __name__ == "__main__":
    build_catalog()
