import os
import requests
from typing import List, Dict

from utils import with_playwright_page


def get_attribute_values(entry: dict, attribute_name: str) -> list:
    return [
        v["text"]
        for attr in entry.get("attributes", [])
        if attr.get("name") == attribute_name
        for v in attr.get("values", [])
    ]


def build_product_json_from_api_entry(entry: dict) -> dict:
    image_id = entry.get("imageId")
    return {
        "product_id": entry["code"],
        "name": entry.get("categories", [{}])[0].get("text", "Unknown"),
        "description": entry.get("description", ""),
        "specs": {
            "hp": get_attribute_values(entry, "output_at_frequency"),
            "voltage": get_attribute_values(entry, "voltage_at_frequency"),
            "rpm": get_attribute_values(entry, "synchronous_speed_at_freq"),
            "frame": next(iter(get_attribute_values(entry, "frame")), ""),
        },
        "bom": [],
        "assets": {
            "DimensionSheet": [],
            "ConnectionDiagram": [],
            "Literature": [],
            "image": f"https://www.baldor.com/AssetImage.axd?id={image_id}" if image_id else "",
        },
    }


def extract_bom_from_parts_tab(product_id: str) -> List[Dict[str, str]]:
    url = f"https://www.baldor.com/catalog/{product_id}#tab=%22parts%22"

    try:
        page, browser, playwright = with_playwright_page(url)
        rows = page.get_by_role("row").all()[1:]
        bom = []

        for row in rows:
            cells = row.get_by_role("cell").all()
            if len(cells) >= 3:
                bom.append(
                    {
                        "part_number": cells[0].inner_text().strip(),
                        "description": cells[1].inner_text().strip(),
                        "quantity": cells[2].inner_text().strip(),
                    }
                )

        browser.close()
        playwright.stop()
        return bom

    except Exception as e:
        print(f"[ERROR] Failed to extract BOM for {product_id}: {e}")
        return []


def download_assets_from_api(product_id: str, headers: dict, timeout: tuple) -> Dict[str, List[str]]:
    url = f"https://www.baldor.com/api/products/{product_id}/drawings"
    asset_dir = os.path.join("output", "assets", product_id)
    os.makedirs(asset_dir, exist_ok=True)

    result = {
        "DimensionSheet": [],
        "ConnectionDiagram": [],
        "Literature": [],
    }

    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        drawings = response.json()

        for drawing in drawings:
            kind = drawing.get("kind")
            number = drawing.get("number")

            if kind not in result:
                continue

            file_url = f"https://www.baldor.com/api/products/{product_id}/drawings/{number}"
            filename = f"{product_id}_{kind}_{number}.pdf"
            save_path = os.path.join(asset_dir, filename)

            try:
                file_response = requests.get(file_url, headers=headers, timeout=timeout)
                file_response.raise_for_status()

                with open(save_path, "wb") as f:
                    f.write(file_response.content)

                print(f"[INFO] Downloaded {kind} for {product_id}: {filename}")
                result[kind].append(save_path)

            except Exception as e:
                print(f"[ERROR] Failed to download {file_url}: {e}")

    except Exception as e:
        print(f"[ERROR] Failed to fetch drawings for {product_id}: {e}")

    return result
