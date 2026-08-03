"""
search.py — searches the Chroma catalog for products similar to a given
piece of text (e.g. the clothing description Gemini generated in vision.py).
"""

import os
import chromadb

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(CURRENT_DIR, "chroma_db")


def search_catalog(query_text: str, n_results: int = 3):
    """
    Find products in the catalog whose descriptions are most similar
    in meaning to query_text.

    Returns a list of dicts like:
        {"product_name": ..., "category": ..., "price": ..., "link": ..., "description": ...}
    """
    client = chromadb.PersistentClient(path=DB_PATH)
    collection = client.get_collection("fashion_catalog")

    results = collection.query(
        query_texts=[query_text],
        n_results=n_results,
    )

    matches = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        matches.append({**meta, "description": doc})
    return matches


if __name__ == "__main__":
    # Quick manual test — searches using a single line of text.
    # Later, this will be the full description vision.py produces.
    test_query = "black blazer for a formal event"
    print(f"Searching for: {test_query}\n")

    for i, match in enumerate(search_catalog(test_query), start=1):
        print(f"{i}. {match['product_name']} (${match['price']}) — {match['category']}")
        print(f"   {match['description']}")
        print()
