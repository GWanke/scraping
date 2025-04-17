import requests
import random
import json


def fetch_baldor_products(config: dict) -> list:
    """
    Fetches the Baldor products from the public API with the config parameters.

    Parameters:
        config (dict): Configuration dictionary with API settings.

    Returns:
        list: List of product entries.
    """
    base_url = "https://www.baldor.com/api/products"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json",
    }

    all_products = []
    total_pages = (config["total_expected"] + config["page_size"] - 1) // config["page_size"]

    for page_index in range(total_pages):
        params = {
            "include": "results",
            "language": "en-US",
            "category": str(config["category_id"]),
            "pageSize": config["page_size"],
            "pageIndex": page_index,
        }

        try:
            response = requests.get(base_url, headers=headers, params=params, timeout=(5, 15))
            response.raise_for_status()
            data = response.json()
            matches = data["results"].get("matches", [])
            all_products.extend(matches)
            print(f"Page {page_index + 1}/{total_pages}: {len(matches)} products collected.")
        except Exception as e:
            print(f"Error on page {page_index + 1}: {e}")

    return all_products


def save_sampled_products(products: list, k: int, output_path: str) -> None:
    """
    Saves a sample of unique products to a JSON file.

    Parameters:
        products (list): Complete product list.
        k (int): Number of products to sample.
        output_path (str): Path to the output JSON file.
    """
    unique_products = {p["code"]: p for p in products}.values()
    sampled = random.sample(list(unique_products), k=min(k, len(unique_products)))

    with open(output_path, "w") as f:
        json.dump(sampled, f, indent=2)

    print(f"{len(sampled)} products saved to: {output_path}")
