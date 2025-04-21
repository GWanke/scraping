import requests
import random
import json


def fetch_baldor_products(config: dict, headers: dict, timeout: tuple) -> list:
    """
    Fetches products from Baldor's API using pagination.
    """
    base_url = "https://www.baldor.com/api/products"
    total_pages = (config["total_expected"] + config["page_size"] - 1) // config["page_size"]
    all_products = []

    for page_index in range(total_pages):
        params = {
            "include": "results",
            "language": "en-US",
            "category": str(config["category_id"]),
            "pageSize": config["page_size"],
            "pageIndex": page_index,
        }

        try:
            response = requests.get(base_url, headers=headers, params=params, timeout=timeout)
            response.raise_for_status()
            matches = response.json()["results"].get("matches", [])
            all_products.extend(matches)
            print(f"[INFO] Page {page_index + 1}/{total_pages}: {len(matches)} products collected.")
        except Exception as e:
            print(f"[ERROR] Page {page_index + 1}: {e}")

    return all_products


def save_sampled_products(products: list, k: int, output_path: str) -> None:
    """
    Saves a random sample of unique products to JSON.
    """
    unique_products = {p["code"]: p for p in products}.values()
    sampled = random.sample(list(unique_products), min(k, len(unique_products)))

    with open(output_path, "w") as f:
        json.dump(sampled, f, indent=2)

    print(f"[INFO] {len(sampled)} products saved to {output_path}")
