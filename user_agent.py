import logging

def load_user_agents(file_path):
    try:
        with open(file_path, 'r') as file:
            user_agents = [line.strip() for line in file.readlines()]
        logging.info("Kullanıcı ajanları başarıyla yüklendi.")
        return user_agents
    except Exception as e:
        logging.error(f"Kullanıcı ajanları dosyası yüklenirken hata: {e}")
        return []
