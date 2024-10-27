import requests

# Dosyayı açıp payload'ları okuyan fonksiyon
def load_payloads(file_path):
    with open(file_path, 'r') as file:
        payloads = [line.strip() for line in file.readlines()]
    return payloads

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
        # GET isteği yapılacak
        test_url = f"{url}{payload}"
        response = requests.get(test_url, headers=headers, timeout=5)
        print(f"GET isteği gönderildi: {test_url}")

        # Yanıt durumu kodunu kontrol et
        print(f"Yanıt durumu: {response.status_code}")

        # Yanıt içeriğini normal yanıt ile karşılaştır
        if response.text != normal_response_content:
            print(f"Muhtemel SQL injection belirtisi! Payload: {payload}")
            print("Normal yanıt ile fark tespit edildi.")
        else:
            print(f"Denendi, ama başarısız oldu. Payload: {payload}")

# Dosya yolunu belirt (Kali için)
file_path = '/home/kullanıcıadi/dosyanınbulunduğudizin/sorgu.txt'

# Payload dosyasını oku
payloads = load_payloads(file_path)

# Hedef URL'yi belirt
target_url = input("Hedef URL'yi girin: ")

# SQL injection testini başlat
test_sql_injection(target_url, payloads)
