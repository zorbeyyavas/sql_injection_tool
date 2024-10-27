# sql_injection_tool


SQL Injection Testing Tool

This Python script is designed to test for SQL injection vulnerabilities by sending GET requests with payloads to a specified URL. Each payload is appended to the target URL and compared to the standard response. If a difference in response is detected, it is flagged as a potential SQL injection vulnerability.

 Features

- Payload Loading: Loads SQL payloads from the `sorgu.txt` file.
- Normal Response Capture: Retrieves a standard response from the URL for reference.
- SQL Injection Testing: Sequentially sends GET requests with payloads, comparing each response to the normal response.
- Difference Detection: Flags a response as a possible SQL injection vulnerability if it differs from the normal response.

Usage

1. Add SQL payloads to your `sorgu.txt` file, with one payload per line.
2. Update the file path in the code to match your local `sorgu.txt` file location.
3. Run the script, input the target URL, and the SQL injection test will start automatically.

 Requirements

- Python 3.x
- `requests` library (install with `pip install requests`)

Türkçe açıklaması 

SQL injection açıklarını test etmek için GET istekleriyle payload’ları hedef URL’ye gönderip normal yanıttan farklı sonuçlar elde etmeye çalıştığı bir sistem şeklinde açıklanabilir. Aşağıda, bu özetle uyumlu olarak README kısmında kullanabileceğiniz bir açıklama bulabilirsiniz:


 SQL Injection Test Aracı

Bu Python betiği, GET istekleri kullanarak belirli bir URL üzerinde SQL injection açıklarını test eder. Bir dizi payload, hedef URL’ye eklenerek istek yapılır ve gelen yanıt, daha önce elde edilen normal yanıtla karşılaştırılır. Farklılık durumunda, bu potansiyel bir SQL injection açığı olarak değerlendirilir.

 Özellikler

- Payload Yükleme: `sorgu.txt` dosyasındaki SQL payload'larını okur.
- Normal Yanıt Alımı: İlk olarak normal yanıt alınır ve referans olarak kaydedilir.
- SQL Injection Testi: Payload’lar sırayla URL’ye GET isteği olarak gönderilir, gelen yanıt normal yanıtla karşılaştırılır.
- Fark Tespiti: Yanıt içeriklerinde farklılık tespit edilirse bu durum potansiyel bir SQL injection açığı olarak rapor edilir.

 Kullanım

1. `sorgu.txt` dosyanızda test etmek istediğiniz SQL payload'larını her satıra bir payload olacak şekilde ekleyin.
2. Kodda belirtilen dosya yolunu kendi sorgu.txt dosyanızın konumuna göre güncelleyin.
3. Çalıştırarak hedef URL'yi girin ve otomatik olarak SQL injection testi başlatın.

 Gereksinimler

- Python 3.x
- `requests` kütüphanesi (`pip install requests` ile kurulabilir)



