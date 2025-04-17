from typing import List, Dict
from utils import with_playwright_page


def get_attribute_values(entry: dict, attribute_name: str) -> list:
    """
    Extracts a list of text values from a product attribute by name.
    """
    for attr in entry.get("attributes", []):
        if attr.get("name") == attribute_name:
            return [v["text"] for v in attr.get("values", [])]
    return []


def build_product_json_from_api_entry(entry: dict) -> dict:
    """
    Builds the final product JSON structure from a raw API entry.
    """
    hp_values = get_attribute_values(entry, "output_at_frequency")
    voltage_values = get_attribute_values(entry, "voltage_at_frequency")
    rpm_values = get_attribute_values(entry, "synchronous_speed_at_freq")
    frame_values = get_attribute_values(entry, "frame")
    image_id = entry.get("imageId")

    return {
        "product_id": entry["code"],
        "name": entry.get("categories", [{}])[0].get("text", "Unknown"),
        "description": entry.get("description", ""),
        "specs": {
            "hp": hp_values,
            "voltage": voltage_values,
            "rpm": rpm_values,
            "frame": frame_values[0] if frame_values else "",
        },
        "bom": [],
        "assets": {
            "manual": "",
            "cad": "",
            "image": (f"https://www.baldor.com/AssetImage.axd?id={image_id}" if image_id else ""),
        },
    }


def extract_bom_from_parts_tab(product_id: str) -> List[Dict[str, str]]:
    """
    Extracts the BOM table from the product 'parts' tab using Playwright.

    Args:
        product_id (str): The product's catalog ID (e.g., DRX14224T).

    Returns:
        list: A list of BOM items, each with part number, description, and quantity.
    """
    tab_url = f"https://www.baldor.com/catalog/{product_id}#tab=%22parts%22"

    try:
        page, browser, playwright = with_playwright_page(tab_url)

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
        print(f"Failed to extract BOM for {product_id}: {e}")
        return []
