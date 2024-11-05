import requests
import logging
import random
from concurrent.futures import ThreadPoolExecutor
from obfuscator import obfuscate_payloads

def get_response(url, headers, method='GET', data=None):
    """
    Belirtilen yönteme göre HTTP isteği yapar ve yanıtı döner.
    GET ve POST yöntemleri desteklenir.
    """
    try:
        if method == 'GET':
            return requests.get(url, headers=headers, timeout=5)
        elif method == 'POST':
            return requests.post(url, headers=headers, data=data, timeout=5)
    except requests.Timeout:
        logging.error("İstek zaman aşımına uğradı.")
    except requests.ConnectionError:
        logging.error("Bağlantı hatası oluştu.")
    except requests.RequestException as e:
        logging.error(f"İstek sırasında hata oluştu: {e}")
    return None

def compare_headers(original_headers, injection_headers):
    """
    Orijinal isteğin header'ları ile injection yapılan isteğin header'larını karşılaştırır.
    Farklılık varsa True döner, yoksa False döner.
    """
    for key in original_headers:
        if key not in injection_headers or original_headers[key] != injection_headers[key]:
            return True
    return False

def check_response(normal_response_content, response, payload, error_messages):
    """
    Gelen yanıt içeriğini normal yanıtla karşılaştırır ve hata mesajlarını kontrol eder.
    Yanıt farklıysa veya hata mesajı içeriyorsa True döner, aksi halde False döner.
    """
    if not response:
        return False
    
    # Yanıt içeriği farklı veya hata mesajları içeriyor mu kontrol edilir
    if response.text != normal_response_content or any(error in response.text for error in error_messages):
        logging.warning(f"SQL Enjeksiyonu başarılı! Payload: {payload}")
        return True
    return False

def test_sql_injection(url, payloads, error_messages, user_agents, is_post=False, data=None):
    """
    SQL enjeksiyon testini yürütür.
    Her bir payload için obfuscation varyasyonları oluşturur ve test eder.
    """
    # Kullanıcı ajanları dosyasından rastgele bir user-agent seçilir
    random_user_agent = random.choice(user_agents) if user_agents else "Mozilla/5.0"
    headers = {'User-Agent': random_user_agent}
    
    # Normal isteği yaparak referans yanıt içeriğini alır
    normal_response = get_response(url, headers, method='POST' if is_post else 'GET', data=data)
    if normal_response:
        normal_response_content = normal_response.text
        original_headers = normal_response.request.headers
        logging.info("Normal yanıt referans olarak alındı.")
    else:
        logging.error("Normal yanıt alınamadı, test gerçekleştirilemiyor.")
        return
    
    # Çoklu iş parçacığı ile test işlemleri
    with ThreadPoolExecutor(max_workers=5) as executor:
        for payload in payloads:
            # Obfuscation ile farklı varyasyonlar oluşturur
            obfuscated_payloads = obfuscate_payloads(payload)

            for obf_payload in obfuscated_payloads:
                # GET isteği için URL'yi oluşturur, POST için veri kısmına ekler
                target_url = f"{url}{obf_payload}" if not is_post else url
                modified_data = data.copy() if data and is_post else None
                if is_post and modified_data is not None:
                    modified_data['injection'] = obf_payload

                # İstek gönderme ve yanıt kontrol etme işlemini iş parçacığına ekler
                future = executor.submit(get_response, target_url, headers, 'POST' if is_post else 'GET', modified_data)
                response = future.result()

                # Yanıt içeriğini ve header'ları karşılaştırır
                if response:
                    header_diff = compare_headers(original_headers, response.request.headers)
                    if check_response(normal_response_content, response, obf_payload, error_messages) or header_diff:
                        logging.info(f"[MUHTEMEL AÇIK] SQL injection başarılı! Payload: {obf_payload}")
                        break
                else:
                    continue
