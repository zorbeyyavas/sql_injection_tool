import requests
import urllib.parse
import argparse
import logging
from concurrent.futures import ThreadPoolExecutor
import json
import random

# Loglama yapılandırması
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_config(config_path):
    # Konfigürasyon dosyasını yükler.
    try:
        with open(config_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        logging.error(f"Konfigürasyon dosyası yüklenirken hata: {e}")
        return {}

def load_payloads(file_path):
    # Belirtilen dosyadan payload'ları yükler.
    try:
        with open(file_path, 'r') as file:
            payloads = [line.strip() for line in file.readlines()]
        logging.info("Payload'lar başarıyla yüklendi.")
        return payloads
    except Exception as e:
        logging.error(f"Payload dosyası yüklenirken hata: {e}")
        return []

def load_error_messages(file_path):
    # Belirtilen dosyadan hata mesajlarını yükler.
    try:
        with open(file_path, 'r') as file:
            errors = [line.strip() for line in file.readlines()]
        logging.info("Hata mesajları başarıyla yüklendi.")
        return errors
    except Exception as e:
        logging.error(f"Hata mesajları dosyası yüklenirken hata: {e}")
        return []

def load_user_agents(file_path):
    # Belirtilen dosyadan kullanıcı ajanlarını yükler.
    try:
        with open(file_path, 'r') as file:
            user_agents = [line.strip() for line in file.readlines()]
        logging.info("Kullanıcı ajanları başarıyla yüklendi.")
        return user_agents
    except Exception as e:
        logging.error(f"Kullanıcı ajanları dosyası yüklenirken hata: {e}")
        return []

def obfuscate_payloads(payload):
    # Payload'ları çeşitli yollarla gizler.
    obfuscations = [
        urllib.parse.quote(payload),  
        "".join([f"%{hex(ord(c))[2:]}" for c in payload]),  
        "||".join(payload.split(" ")),  
        payload.replace(" ", "/**/"),  
        payload + "--",  
        "/**/".join(payload.split(" ")),  
    ]
    if "UNION" in payload:
        obfuscations.append(payload.replace("UNION", "UNION/**/"))
    if "SELECT" in payload:
        obfuscations.append(payload.replace("SELECT", "SELECT/**/"))
    
    return obfuscations

def get_response(url, headers, method='GET', data=None):
    # GET veya POST isteği yapar ve yanıtı döndürür.
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers, timeout=5)
        elif method == 'POST':
            response = requests.post(url, headers=headers, data=data, timeout=5)
        return response
    except requests.Timeout:
        logging.error("Zaman aşımına uğradı.")
        return None
    except requests.ConnectionError:
        logging.error("Bağlantı hatası.")
        return None
    except requests.RequestException as e:
        logging.error(f"İstek sırasında hata: {e}")
        return None

def check_response(normal_response, response, payload, error_messages):
    # Yanıtı normal yanıt ile karşılaştırır ve hata mesajlarını kontrol eder.
    response_different = response.text != normal_response
    error_detected = any(error in response.text for error in error_messages)
    
    # Yanıt süresi, durum kodu ve yanıt boyutunu kontrol et
    response_time = response.elapsed.total_seconds() if response else None
    response_code = response.status_code if response else None
    response_size = len(response.text) if response else None

    # Her iki durumdan birinin sağlanması yeterli
    if response_different or error_detected:
        logging.warning(f"SQL Enjeksiyonu Başarılı! Payload: {payload}")
        logging.info(f"Yanıt Süresi: {response_time}s, HTTP Durum Kodu: {response_code}, Yanıt Boyutu: {response_size} byte")
        return True  # SQL injection detected
    
    return False

def test_sql_injection(url, payloads, error_messages, user_agents, is_post=False, data=None):
    # SQL injection açığını test eden fonksiyonu.
    random_user_agent = random.choice(user_agents) if user_agents else {}
    headers = {'User-Agent': random_user_agent}  # Rastgele User-Agent ekle
    normal_response = get_response(url, headers, method='POST' if is_post else 'GET', data=data)
    normal_response_content = normal_response.text if normal_response else ""
    logging.info("Normal yanıt alındı ve referans olarak kaydedildi.")

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for payload in payloads:
            obfuscated_payloads = obfuscate_payloads(payload)
            for obf_payload in obfuscated_payloads:
                test_url = f"{url}{obf_payload}" if not is_post else url
                modified_data = data.copy() if is_post else {}
                if is_post:
                    modified_data['payload'] = obf_payload  # Payload'ı POST verisine ekle
                futures.append(executor.submit(get_response, test_url, headers, method='POST' if is_post else 'GET', data=modified_data))

        for future, payload in zip(futures, payloads):
            response = future.result()
            if check_response(normal_response_content, response, payload, error_messages):
                # SQL injection detected
                logging.info(f"SQL injection testi başarılı! Payload: {payload}")
            else:
                logging.info(f"SQL injection testi başarısız! Payload: {payload}")  

def main():
    # Ana fonksiyon
    parser = argparse.ArgumentParser(description='SQL Injection Tester')
    parser.add_argument('-g', '--url', required=True, help='Hedef URL')
    parser.add_argument('-p', '--post', action='store_true', help='POST isteklerini kullan')
    parser.add_argument('-d', '--data', type=str, help='POST verileri (örneğin: username=test&password=test)')
    parser.add_argument('-c', '--config', type=str, help='Konfigürasyon dosyası')
    args = parser.parse_args()

    config = load_config(args.config) if args.config else {}
    
    payload_file_path = config.get('payloads_file', '/home/kullanıcıadı/Dosyayolu/sorgu.txt')
    error_file_path = config.get('errors_file', '/home/kullanıcıadı/Dosyayolu/errors.txt')
    user_agent_file_path = '/home/kullanıcıadı/Dosyayolu/user-agents.txt'

    payloads = load_payloads(payload_file_path)
    error_messages = load_error_messages(error_file_path)
    user_agents = load_user_agents(user_agent_file_path)

    post_data = {}
    if args.data:
        post_data = dict(item.split('=') for item in args.data.split('&'))

    test_sql_injection(args.url, payloads, error_messages, user_agents, is_post=args.post, data=post_data)

if __name__ == "__main__":
    main()
