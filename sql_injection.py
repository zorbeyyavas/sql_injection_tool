import logging
import random
from concurrent.futures import ThreadPoolExecutor
import payload, htt

def check_response(normal_response, response, payload, error_messages):
    response_different = response.text != normal_response
    error_detected = any(error in response.text for error in error_messages)
    response_time = response.elapsed.total_seconds() if response else None
    response_code = response.status_code if response else None
    response_size = len(response.text) if response else None

    if response_different or error_detected:
        logging.warning(f"SQL Enjeksiyonu Başarılı! Payload: {payload}")
        logging.info(f"Yanıt Süresi: {response_time}s, HTTP Durum Kodu: {response_code}, Yanıt Boyutu: {response_size} byte")
        return True
    
    return False

def test_sql_injection(url, payloads, error_messages, user_agents, is_post=False, data=None):
    random_user_agent = random.choice(user_agents) if user_agents else {}
    headers = {'User-Agent': random_user_agent}
    normal_response = htt.get_response(url, headers, method='POST' if is_post else 'GET', data=data)
    normal_response_content = normal_response.text if normal_response else ""
    logging.info("Normal yanıt alındı ve referans olarak kaydedildi.")

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for payload_text in payloads:
            obfuscated_payloads = payload.obfuscate_payloads(payload_text)
            for obf_payload in obfuscated_payloads:
                test_url = f"{url}{obf_payload}" if not is_post else url
                modified_data = data.copy() if is_post else {}
                if is_post:
                    modified_data['payload'] = obf_payload
                futures.append(executor.submit(htt.get_response, test_url, headers, method='POST' if is_post else 'GET', data=modified_data))

        for future, payload_text in zip(futures, payloads):
            response = future.result()
            if check_response(normal_response_content, response, payload_text, error_messages):
                logging.info(f"SQL injection testi başarılı! Payload: {payload_text}")
            else:
                logging.info(f"SQL injection testi başarısız! Payload: {payload_text}")
