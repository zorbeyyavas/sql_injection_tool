# sql_injection_tool



 SQL Injection Test Tool

This Python script is designed to detect SQL injection vulnerabilities by sending GET requests with various payloads and obfuscation techniques to a specified URL. Each payload is appended to the target URL, and the response is compared with a standard response. If a discrepancy is detected, it’s flagged as a potential SQL injection vulnerability.

Features

- Payload Loading: Reads SQL payloads from the specified `sorgu.txt` file.
- Normal Response Capture: Retrieves and stores a reference response from the target URL.
- Obfuscation Techniques: Applies multiple methods on each payload to bypass potential security filters.
- SQL Injection Testing: Sequentially sends GET requests with each payload and compares responses to the standard response.
- Difference Detection: Flags discrepancies in responses as potential SQL injection vulnerabilities.

Usage

1. Add SQL payloads to your `sorgu.txt` file, with each payload on a new line.
2. Update the file path in the code to match your `sorgu.txt` file location.
3. Run the script, enter the target URL, and the SQL injection test will automatically begin.

Requirements

- Python 3.x
- `requests` library (install with `pip install requests`)



SQL Injection Test Aracı

Bu Python betiği, GET istekleri kullanarak belirli bir URL üzerinde SQL injection açıklarını test eder. Kod, çeşitli payload’lara ek olarak farklı obfuscation (gizleme) yöntemlerini de kullanarak SQL güvenlik filtrelerini aşmayı hedefler. Her payload, hedef URL’ye eklenerek istek yapılır ve gelen yanıt, referans alınan normal yanıtla karşılaştırılır. Farklılık durumunda, bu potansiyel bir SQL injection açığı olarak değerlendirilir.

Özellikler

- Payload Yükleme: `sorgu.txt` dosyasından SQL payload'larını okur.
- Normal Yanıt Alımı: Hedef URL'den ilk olarak referans alınan normal yanıt kaydedilir.
- Obfuscation Yöntemleri: Güvenlik filtrelerinden kaçmak için payload’lara çeşitli gizleme teknikleri uygulanır.
- SQL Injection Testi: Payload’ları sırasıyla URL’ye ekleyerek GET istekleri gönderir ve gelen yanıt normal yanıtla karşılaştırılır.
- Fark Tespiti: Yanıt içeriklerinde farklılık tespit edilirse, bu durum potansiyel bir SQL injection açığı olarak rapor edilir.

Kullanım

1. `sorgu.txt` dosyanızda test etmek istediğiniz SQL payload'larını her satıra bir payload olacak şekilde ekleyin.
2. Kodda belirtilen dosya yolunu kendi `sorgu.txt` dosyanızın konumuna göre güncelleyin.
3. Betiği çalıştırarak hedef URL'yi girin ve SQL injection testi otomatik olarak başlatılacaktır.

Gereksinimler

- Python 3.x
- `requests` kütüphanesi (Kurmak için: `pip install requests`)







