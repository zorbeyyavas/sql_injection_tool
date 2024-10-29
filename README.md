# sql_injection_tool



This Python script is designed to detect SQL injection vulnerabilities by sending GET requests with various payloads and obfuscation techniques to a specified URL. Each payload is appended to the target URL, and the response is compared with a standard response. If a discrepancy is detected, it’s flagged as a potential SQL injection vulnerability.

Features
Payload Loading: Reads SQL payloads from the specified sorgu.txt file.
Normal Response Capture: Retrieves and stores a reference response from the target URL.
Obfuscation Techniques: Applies multiple methods on each payload to bypass potential security filters, including URL encoding, hex encoding, and comment injection.
SQL Injection Testing: Sequentially sends GET requests with each payload and compares responses to the standard response.
Difference Detection: Flags discrepancies in responses as potential SQL injection vulnerabilities.
Usage
Add SQL payloads to your sorgu.txt file, with each payload on a new line.

Update the file_path variable in the code to match your sorgu.txt file location.

Run the script with the target URL as a command line argument:


python sqli_tool.py -g <TARGET_URL>
Replace <TARGET_URL> with the URL you want to test.

Requirements
Python 3.x
requests library (Install with pip install requests)
Example
To run the tool, use the following command:


python sqli_tool.py -g http://example.com/page?id=
This command will test the specified URL for SQL injection vulnerabilities using the payloads defined in your sorgu.txt file.


SQL Injection Test Aracı
Bu Python betiği, GET istekleri kullanarak belirli bir URL üzerinde SQL injection açıklarını test eder. Kod, çeşitli payload’lara ek olarak farklı obfuscation (gizleme) yöntemlerini de kullanarak SQL güvenlik filtrelerini aşmayı hedefler. Her payload, hedef URL’ye eklenerek istek yapılır ve gelen yanıt, referans alınan normal yanıtla karşılaştırılır. Farklılık durumunda, bu potansiyel bir SQL injection açığı olarak değerlendirilir.

Özellikler
Payload Yükleme: sorgu.txt dosyasından SQL payload'larını okur.
Normal Yanıt Alımı: Hedef URL'den ilk olarak referans alınan normal yanıt kaydedilir.
Obfuscation Yöntemleri: Güvenlik filtrelerinden kaçmak için payload’lara çeşitli gizleme teknikleri uygulanır, URL kodlaması, hex kodlama ve yorum enjekte etme dahil.
SQL Injection Testi: Payload’ları sırasıyla URL’ye ekleyerek GET istekleri gönderir ve gelen yanıt normal yanıtla karşılaştırılır.
Fark Tespiti: Yanıt içeriklerinde farklılık tespit edilirse, bu durum potansiyel bir SQL injection açığı olarak rapor edilir.
Kullanım
sorgu.txt dosyanıza test etmek istediğiniz SQL payload'larını her satıra bir payload olacak şekilde ekleyin.

Kodda belirtilen file_path değişkenini kendi sorgu.txt dosyanızın konumuna göre güncelleyin.

Betiği hedef URL'yi komut satırı argümanı olarak vererek çalıştırın:


python sqli_tool.py -g <HEDEF_URL>
<HEDEF_URL> kısmını test etmek istediğiniz URL ile değiştirin.

Gereksinimler
Python 3.x
requests kütüphanesi (Kurmak için: pip install requests)
Örnek
Aracı çalıştırmak için aşağıdaki komutu kullanın:

python sqli_tool.py -g http://example.com/page?id=
Bu komut, belirtilen URL'yi sorgu.txt dosyanızda tanımlı payload'ları kullanarak SQL injection açıkları için test edecektir.





