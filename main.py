import json

# Carrega config
with open("config.json") as f:
    CONFIG = json.load(f)

START_URL = CONFIG["start_url"]
OUTPUT_DIR = CONFIG["output_dir"]
ASSETS_DIR = f"{OUTPUT_DIR}/{CONFIG['assets_subdir']}"
LINKS_PATH = f"{OUTPUT_DIR}/{CONFIG['links_file']}"
PRODUCT_LIMIT = CONFIG["product_limit"]
