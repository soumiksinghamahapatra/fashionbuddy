"""
text_search.py — Phase 4: the text query flow.

Instead of uploading a photo, the user types what they're looking for
(e.g. "a dress for a formal dinner") and we search the same catalog
used by the image flow.

This reuses search.py — the same vector search Phase 2 built — so
there's nothing new to install or set up.
"""

from search import search_catalog


def recommend_from_text(query: str, n_results: int = 3):
    print(f'Searching for: "{query}"\n')

    matches = search_catalog(query, n_results=n_results)

    if not matches:
        print("No matching products found.")
        return

    print("Recommended from our catalog:")
    for m in matches:
        print(f"- {m['product_name']} (${m['price']}) — {m['category']}")
        print(f"  {m['description']}")
        print(f"  {m['link']}\n")


if __name__ == "__main__":
    # input() pauses the program and waits for you to type something
    # and press Enter — this is what makes it interactive.
    user_query = input("What are you looking for? ")
    recommend_from_text(user_query)
