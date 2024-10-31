import logging

def load_error_messages(file_path):
    try:
        with open(file_path, 'r') as file:
            errors = [line.strip() for line in file.readlines()]
        logging.info("Hata mesajları başarıyla yüklendi.")
        return errors
    except Exception as e:
        logging.error(f"Hata mesajları dosyası yüklenirken hata: {e}")
        return []
