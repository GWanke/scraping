import json
import os
from fetch_data_from_api import fetch_baldor_products, save_sampled_products
from parser import build_product_json_from_api_entry, extract_bom_from_parts_tab


def main():
    """
    Main function to orchestrate data collection and processing .
    """
    with open("config/config.json", "r") as f:
        config = json.load(f)

    all_products = fetch_baldor_products(config)
    save_sampled_products(all_products, config["samples_to_extract"], config["output_path"])

    with open(config["output_path"], "r") as f:
        sampled_products = json.load(f)

    output_dir = "output/products"
    os.makedirs(output_dir, exist_ok=True)

    for entry in sampled_products:
        parsed = build_product_json_from_api_entry(entry)
        parsed["bom"] = extract_bom_from_parts_tab(parsed["product_id"])

        out_path = os.path.join(output_dir, f"{parsed['product_id']}.json")
        with open(out_path, "w") as f_out:
            json.dump(parsed, f_out, indent=2)

        print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
