SQL Injection Testing Tool

This Python tool is designed to detect SQL injection vulnerabilities on specified URLs by sending GET or POST requests with various payloads and obfuscation techniques. The tool sends requests with each payload to the target URL, compares responses to a standard response, and flags any discrepancies as potential SQL injection vulnerabilities.

Features

- Payload Loading: Reads SQL payloads from the specified `sorgu.txt` file.
- Normal Response Capture: Retrieves an initial reference response, used as a baseline to compare subsequent responses.
- Obfuscation Techniques: Applies various methods to obfuscate payloads, including URL encoding, hex encoding, and comment injection.
- SQL Injection Testing: Sequentially appends each payload to the URL and sends GET or POST requests, then compares responses to the baseline.
- Error Message Detection: Compares responses against known error messages loaded from `errors.txt` to detect SQL injection vulnerabilities.
- Response Difference Analysis: Flags differences in content or size as potential SQL injection vulnerabilities.
- Parallel Processing with ThreadPoolExecutor: Enhances testing speed by sending multiple requests concurrently.

Requirements

- Python 3.x
- `requests` library (Install with: `pip install requests`)

Usage

1. Add SQL Payloads: Add SQL payloads to `sorgu.txt`, with each payload on a new line.
2. Add Error Messages: Add known error messages to `errors.txt`, with each message on a new line.
3. Update File Paths: Adjust `file_path` variables in the code to match the paths of your `sorgu.txt` and `errors.txt` files.

Running from Command Line

You can run the tool with the following command:

python sqli_tool.py -g <TARGET_URL> [-p] [-d <POST_DATA>] [-c <CONFIG_FILE>]


Parameters

- `-g --url` (required): Target URL.
- `-p --post`: Use for POST requests (GET is the default).
- `-d --data`: Data to be sent in POST request, e.g., `username=test&password=test`.
- `-c --config`: Configuration file (optional). 

Example Usage


python sqli_tool.py -g http://example.com/page?id=


This command tests the specified URL for SQL injection using payloads defined in `sorgu.txt` and known error messages in `errors.txt`.



Details

Main Functions

1. `load_config`: Loads configuration file in JSON format.
2. `load_payloads` / `load_error_messages` / `load_user_agents`**: Loads payloads, error messages, and user agents from respective files.
3. `obfuscate_payloads`: Modifies payloads using various obfuscation techniques.
4. `get_response`: Sends a GET or POST request to the target URL.
5. `check_response`: Analyzes the response and checks for SQL injection indicators.
6. `test_sql_injection`: Tests all payloads on the target URL and evaluates SQL injection results.

Response Analysis

The tool uses these response analysis methods:
- Response Time: Longer-than-expected response times can indicate SQL injection.
- HTTP Status Code: Differences in response codes are a key indicator.
- Response Size: Responses larger or smaller than expected may signal injection.


Türkçe Versiyon

SQL Enjeksiyon Test Aracı

Bu Python aracı, belirli URL’ler üzerinde SQL enjeksiyon açıklıklarını tespit etmek için GET veya POST istekleri gönderir. Araç, çeşitli payload’ları hedef URL’ye ekleyerek yanıtları referans alınan bir yanıtla karşılaştırır ve farklılıkları potansiyel SQL enjeksiyon açıklıkları olarak işaretler.

Özellikler

- Payload Yükleme: SQL payload'larını belirtilen `sorgu.txt` dosyasından okur.
- Normal Yanıt Alımı: İlk olarak referans olarak alınan bir yanıtı kaydeder, bu yanıt sonraki yanıtlarla karşılaştırılır.
- Obfuscation Teknikleri: URL kodlama, hex kodlama, yorum enjekte etme gibi çeşitli gizleme teknikleri kullanarak güvenlik filtrelerinden kaçmayı amaçlar.
- SQL Enjeksiyon Testi: Payload’ları sırasıyla URL’ye ekleyerek GET veya POST istekleri gönderir ve yanıtları referans yanıtla karşılaştırır.
- Hata Mesajı Tespiti: Gelen yanıtları `errors.txt` dosyasındaki bilinen hata mesajları ile karşılaştırarak SQL enjeksiyon açıklıklarını tespit eder.
- Yanıt Farklılıklarını İnceleme: Yanıt içeriklerinde veya boyutunda farklılık tespit edilirse, bu potansiyel bir SQL enjeksiyonu olarak işaretlenir.
- ThreadPoolExecutor ile Paralel İşlem: Birden fazla isteği eşzamanlı göndererek test sürecini hızlandırır.

Gereksinimler

- Python 3.x
- `requests` kütüphanesi (Kurulum için: `pip install requests`)

Kullanım

1. SQL Payloadları Ekleme: Her satırda bir payload olacak şekilde `sorgu.txt` dosyasını güncelleyin.
2. Hata Mesajlarını Ekleme: Bilinen hata mesajlarını `errors.txt` dosyasına her satırda bir hata mesajı olacak şekilde ekleyin.
3. Dosya Konumlarını Güncelleyin: Kod içindeki `file_path` değişkenlerini, `sorgu.txt` ve `errors.txt` dosyalarınızın konumuna göre güncelleyin.

Komut Satırından Çalıştırma

Aşağıdaki komutu kullanarak aracı çalıştırabilirsiniz:


python sqli_tool.py -g <HEDEF_URL> [-p] [-d <POST_VERİLERİ>] [-c <KONFİGÜRASYON_DOSYASI>]


Parametreler

- `-g --url` (gerekli): Hedef URL.
- `-p --post`: POST istekleri için kullanılır (varsayılan GET'tir).
- `-d --data`: POST verisi olarak gönderilecek parametreler, örneğin `username=test&password=test`.
- `-c --config`: Konfigürasyon dosyası (isteğe bağlı). 

Örnek Kullanım


python sqli_tool.py -g http://example.com/page?id=


Bu komut, `sorgu.txt` dosyasındaki payload'ları ve `errors.txt` dosyasındaki hata mesajlarını kullanarak belirtilen URL’yi SQL enjeksiyon açıklıkları için test eder.


Detaylar

Ana İşlevler

1. `load_config`: JSON formatındaki konfigürasyon dosyasını yükler.
2. `load_payloads` / `load_error_messages` / `load_user_agents`**: Payload, hata mesajları ve kullanıcı ajanlarını ilgili dosyalardan yükler.
3. `obfuscate_payloads`**: Çeşitli gizleme teknikleri kullanarak payload'ları modifiye eder.
4. `get_response`: Hedef URL'ye GET veya POST isteği gönderir.
5. `check_response`: Yanıtı analiz eder ve SQL enjeksiyon belirtilerini kontrol eder.
6. `test_sql_injection`: Tüm payload'ları hedef URL üzerinde test eder ve SQL enjeksiyon sonuçlarını değerlendirir.

Yanıt Analizi

Aracın yanıtları analiz etme yöntemleri şunlardır:
- Yanıt Süresi: Beklenenden uzun yanıt süreleri SQL enjeksiyonu belirtisi olabilir.
- HTTP Durum Kodu: Yanıt kodundaki farklılıklar önemli bir göstergedir.
- Yanıt Boyutu: Beklenenden büyük veya küçük yanıtlar enjeksiyonu işaret edebilir.

