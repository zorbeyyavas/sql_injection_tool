import json
import logging

def load_config(config_path):
    """
    Konfigürasyon dosyasını JSON formatında yükler.
    Eksik veya bozuk dosya durumunda boş bir sözlük döner.
    """
    try:
        with open(config_path, 'r') as file:
            config_data = json.load(file)
            logging.info("Konfigürasyon dosyası başarıyla yüklendi.")
            return config_data
    except FileNotFoundError:
        logging.error(f"Konfigürasyon dosyası bulunamadı: {config_path}")
    except json.JSONDecodeError:
        logging.error("Konfigürasyon dosyası bozuk veya geçersiz JSON formatında.")
    except Exception as e:
        logging.error(f"Konfigürasyon dosyası yüklenirken beklenmeyen hata: {e}")
    return {}  # Hata durumunda boş bir sözlük döner.
