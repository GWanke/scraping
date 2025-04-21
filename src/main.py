import json
import os

from fetch_data_from_api import fetch_baldor_products, save_sampled_products
from parser import (
    build_product_json_from_api_entry,
    extract_bom_from_parts_tab,
    download_assets_from_api,
)


def main():
    """
    Main pipeline to orchestrate the data collection, transformation, and enrichment
    of Baldor motor product information.
    """
    with open("config/config.json", "r") as f:
        config = json.load(f)

    headers = config["headers"]
    timeout = tuple(config["timeout"])
    output_dir = "output/products"
    os.makedirs(output_dir, exist_ok=True)

    products = fetch_baldor_products(config, headers, timeout)
    save_sampled_products(products, config["samples_to_extract"], config["output_path"])

    with open(config["output_path"], "r") as f:
        sampled_products = json.load(f)

    for entry in sampled_products:
        product_id = entry["code"]
        product_data = build_product_json_from_api_entry(entry)
        product_data["bom"] = extract_bom_from_parts_tab(product_id)
        product_data["assets"] = download_assets_from_api(product_id, headers, timeout)

        out_path = os.path.join(output_dir, f"{product_id}.json")
        with open(out_path, "w") as f_out:
            json.dump(product_data, f_out, indent=2)

        print(f"[INFO] Product saved to {out_path}")


if __name__ == "__main__":
    main()
