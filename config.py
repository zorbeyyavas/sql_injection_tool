import json
import logging

def load_config(config_path):
    try:
        with open(config_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        logging.error(f"Konfigürasyon dosyası yüklenirken hata: {e}")
        return {}
