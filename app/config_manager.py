import json

CONFIG_FILE = "config.json"

def load_config():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_config(image_folder, output_csv):
    config = {"image_folder": image_folder, "output_csv": output_csv}
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
