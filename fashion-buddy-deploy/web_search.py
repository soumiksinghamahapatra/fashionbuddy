"""
web_search.py — searches the real internet for real, buyable products,
prioritizing Indian shopping sites. Uses Tavily (free tier).
"""

import os
import requests
from tavily import TavilyClient

client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))

INDIAN_SHOPPING_SITES = [
    "amazon.in",
    "flipkart.com",
    "myntra.com",
    "ajio.com",
    "nykaafashion.com",
    "tatacliq.com",
]


def _extract(response) -> list:
    results = []
    for r in response.get("results", []):
        snippet = (r.get("content") or "")[:220]
        results.append({
            "product_name": r.get("title", "Product"),
            "description": snippet,
            "link": r.get("url", ""),
            "price": None,
        })
    return results


def find_products(query: str, max_results: int = 3, indian_sites_only: bool = True):
    if indian_sites_only:
        response = client.search(
            query=f"buy {query} India",
            max_results=max_results,
            search_depth="basic",
            include_domains=INDIAN_SHOPPING_SITES,
        )
        results = _extract(response)
        if results:
            return results

    response = client.search(query=f"buy {query}", max_results=max_results, search_depth="basic")
    return _extract(response)


def find_garment_with_image(query: str, indian_sites_only: bool = True):
    search_kwargs = dict(
        query=f"buy {query} India",
        search_depth="basic",
        include_images=True,
        max_results=5,
    )
    if indian_sites_only:
        search_kwargs["include_domains"] = INDIAN_SHOPPING_SITES

    response = client.search(**search_kwargs)
    images = response.get("images", [])
    results = response.get("results", [])

    if not images and indian_sites_only:
        response = client.search(query=f"buy {query}", search_depth="basic", include_images=True, max_results=5)
        images = response.get("images", [])
        results = response.get("results", [])

    if not images:
        return None

    first_image = images[0]
    image_url = first_image if isinstance(first_image, str) else first_image.get("url")

    return {
        "image_url": image_url,
        "product_link": results[0]["url"] if results else None,
        "product_title": results[0]["title"] if results else query,
    }


def _is_valid_image(url: str) -> bool:
    """Quick check that a URL actually points to a real, loadable image."""
    try:
        resp = requests.head(url, timeout=4, allow_redirects=True)
        content_type = resp.headers.get("Content-Type", "")
        content_length = int(resp.headers.get("Content-Length", 0) or 0)
        return content_type.startswith("image/") and (content_length == 0 or content_length > 8000)
    except Exception:
        return False


def find_garment_options(query: str, max_results: int = 4, indian_sites_only: bool = True):
    """Returns several candidate products with validated images for the user to pick from."""
    search_kwargs = dict(
        query=f"buy {query} India",
        search_depth="basic",
        include_images=True,
        include_image_descriptions=True,
        max_results=max_results + 4,  # fetch extras since some get filtered out
    )
    if indian_sites_only:
        search_kwargs["include_domains"] = INDIAN_SHOPPING_SITES

    response = client.search(**search_kwargs)
    images = response.get("images", [])
    results = response.get("results", [])

    if not images and indian_sites_only:
        response = client.search(
            query=f"buy {query}",
            search_depth="basic",
            include_images=True,
            include_image_descriptions=True,
            max_results=max_results + 4,
        )
        images = response.get("images", [])
        results = response.get("results", [])

    options = []
    for i, img in enumerate(images):
        if len(options) >= max_results:
            break
        image_url = img if isinstance(img, str) else img.get("url")
        if not image_url or not _is_valid_image(image_url):
            continue
        img_desc = "" if isinstance(img, str) else img.get("description", "")
        result = results[i] if i < len(results) else (results[0] if results else {})
        options.append({
            "image_url": image_url,
            "product_link": result.get("url"),
            "product_title": result.get("title") or img_desc or query,
        })
    return options
