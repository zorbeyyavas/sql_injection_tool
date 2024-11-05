import logging

def load_payloads(file_path):
    """
    Payload dosyasını yükler ve liste olarak döner.
    Dosya bulunamazsa veya boşsa boş bir liste döner.
    """
    try:
        with open(file_path, 'r') as file:
            payloads = [line.strip() for line in file if line.strip()]
        if payloads:
            logging.info("Payload'lar başarıyla yüklendi.")
            return payloads
        else:
            logging.warning("Payload dosyası boş.")
    except FileNotFoundError:
        logging.error(f"Payload dosyası bulunamadı: {file_path}")
    except Exception as e:
        logging.error(f"Payload dosyası yüklenirken hata: {e}")
    return []

def load_error_messages(file_path):
    """
    Hata mesajları dosyasını yükler ve liste olarak döner.
    Dosya bulunamazsa veya boşsa boş bir liste döner.
    """
    try:
        with open(file_path, 'r') as file:
            errors = [line.strip() for line in file if line.strip()]
        if errors:
            logging.info("Hata mesajları başarıyla yüklendi.")
            return errors
        else:
            logging.warning("Hata mesajları dosyası boş.")
    except FileNotFoundError:
        logging.error(f"Hata mesajları dosyası bulunamadı: {file_path}")
    except Exception as e:
        logging.error(f"Hata mesajları yüklenirken hata: {e}")
    return []

def load_user_agents(file_path):
    """
    Kullanıcı ajanlarını yükler ve liste olarak döner.
    Dosya bulunamazsa veya boşsa boş bir liste döner.
    """
    try:
        with open(file_path, 'r') as file:
            user_agents = [line.strip() for line in file if line.strip()]
        if user_agents:
            logging.info("User-agent'lar başarıyla yüklendi.")
            return user_agents
        else:
            logging.warning("User-agent dosyası boş.")
    except FileNotFoundError:
        logging.error(f"User-agent dosyası bulunamadı: {file_path}")
    except Exception as e:
        logging.error(f"User-agent dosyası yüklenirken hata: {e}")
    return []
