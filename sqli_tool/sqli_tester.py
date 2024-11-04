import requests
import logging
import random
from obfuscator import obfuscate_payloads

def get_response(url, headers, method='GET', data=None):
    """
    Belirtilen yöntemde HTTP isteği yapar ve yanıtı döner.
    """
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers, timeout=5)
        else:
            response = requests.post(url, headers=headers, data=data, timeout=5)
    except requests.RequestException as e:
        logging.error(f"HTTP isteği sırasında hata: {e}")
        return None
    return response

def compare_headers(original_headers, injection_headers):
    """
    İki set header'ı karşılaştırır.
    """
    for key in original_headers:
        if key not in injection_headers or original_headers[key] != injection_headers[key]:
            return True
    return False

def test_sql_injection(url, payloads, error_messages, user_agents, is_post=False, data=None):
    """
    SQL enjeksiyon testini gerçekleştirir.
    """
    original_response = get_response(url, {'User-Agent': random.choice(user_agents)}, method='POST' if is_post else 'GET', data=data)
    if original_response is None:
        logging.error("Orijinal isteğe yanıt alınamadı.")
        return

    original_headers = original_response.request.headers
    original_content = original_response.text

    for payload in payloads:
        obfuscated_payloads = obfuscate_payloads(payload)

        for obfuscated_payload in obfuscated_payloads:
            injected_url = f"{url}{obfuscated_payload}"
            injection_response = get_response(injected_url, {'User-Agent': random.choice(user_agents)}, method='POST' if is_post else 'GET', data=data)

            if injection_response is None:
                continue

            injection_headers = injection_response.request.headers
            header_diff = compare_headers(original_headers, injection_headers)

            if header_diff:
                logging.info(f"[UYARI] Header farklılığı bulundu: {injected_url}")

            if injection_response.text != original_content:
                logging.info(f"[UYARI] Yanıt içeriği farklı: {injected_url}")
                for error in error_messages:
                    if error in injection_response.text:
                        logging.info(f"[HATA BULUNDU] Hata mesajı tespit edildi: {injected_url} - {error}")

            # Meta veri karşılaştırması
            if header_diff or injection_response.text != original_content:
                logging.info(f"[MUHTEMEL AÇIK] Potansiyel SQL enjeksiyon açığı bulundu: {injected_url}")
