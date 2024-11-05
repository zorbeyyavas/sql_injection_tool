SQL Enjeksiyon Test Aracı

Bu Python tabanlı SQL Enjeksiyon Test Aracı, belirtilen URL'lerde SQL enjeksiyon açıklıklarını tespit etmek amacıyla GET veya POST istekleri gönderir. Araç, hedef URL’ye çeşitli SQL enjeksiyon payload’larını ekleyerek yanıtları analiz eder. Yanıtlar, referans bir yanıt ile karşılaştırılarak farklılıklar potansiyel SQL enjeksiyon açıklıkları olarak işaretlenir.

Özellikler
Payload Yükleme: Araç, SQL payload'larını sorgu.txt dosyasından okur.
Normal Yanıt Alımı: Referans olarak alınan ilk yanıtı kaydederek sonraki yanıtları bu referans yanıtla karşılaştırır.
Obfuscation Teknikleri: SQL enjeksiyon payload'ları üzerinde URL kodlama, hex kodlama, SQL yorumları ekleme gibi çeşitli gizleme teknikleri uygulanır.
SQL Enjeksiyon Testi: Payload’ları sırasıyla URL’ye ekleyerek GET veya POST istekleri gönderir ve yanıtları referans yanıtla karşılaştırır.
Hata Mesajı Tespiti: Yanıtlar, errors.txt dosyasındaki bilinen hata mesajları ile karşılaştırılarak SQL enjeksiyon açıklıklarını tespit eder.
Yanıt Farklılıklarını İnceleme: Yanıtların içeriğinde veya header meta verilerinde farklılık tespit edilirse, bu durum potansiyel bir SQL enjeksiyonu olarak işaretlenir.
ThreadPoolExecutor ile Paralel İşlem: Birden fazla isteği eşzamanlı olarak göndererek test sürecini hızlandırır.

Gereksinimler

Python 3.x
requests kütüphanesi (Kurulum için: pip install requests)

Kurulum ve Kullanım

SQL Payloadları Ekleme: Her satırda bir payload olacak şekilde sorgu.txt dosyasını güncelleyin.
Hata Mesajlarını Ekleme: Bilinen hata mesajlarını errors.txt dosyasına her satırda bir hata mesajı olacak şekilde ekleyin.
Kullanıcı Ajanlarını Ekleme: user-agents.txt dosyasına kullanılacak olan user-agent'ları ekleyin.


Komut Satırından Çalıştırma
Aşağıdaki komutu kullanarak aracı çalıştırabilirsiniz:
python main.py -g <HEDEF_URL> [-p] [-d <POST_VERİLERİ>] [-c <KONFİGÜRASYON_DOSYASI>]


Parametreler
-g, --url (gerekli): Hedef URL.
-p, --post: POST istekleri için kullanılır (varsayılan GET'tir).
-d, --data: POST verisi olarak gönderilecek parametreler, örneğin username=test&password=test.
-c, --config: Konfigürasyon dosyası (isteğe bağlı).

Örnek Kullanım
python main.py -g http://example.com/page?id=

Bu komut, sorgu.txt dosyasındaki payload'ları ve errors.txt dosyasındaki hata mesajlarını kullanarak belirtilen URL’yi SQL enjeksiyon açıklıkları için test eder.




SQL Injection Testing Tool

This Python-based SQL Injection Testing Tool sends GET or POST requests to specified URLs to identify SQL injection vulnerabilities. The tool appends various SQL injection payloads to the target URL and analyzes the responses. Responses are compared to a reference response to identify differences that may indicate potential SQL injection vulnerabilities.

Features
- Payload Loading: The tool reads SQL payloads from the `sorgu.txt` file.
- Normal Response Acquisition: The first response is saved as a reference, and subsequent responses are compared to this reference response.
- Obfuscation Techniques: Various obfuscation techniques, such as URL encoding, hex encoding, and adding SQL comments, are applied to SQL injection payloads.
- SQL Injection Testing: Payloads are sequentially appended to the URL to send GET or POST requests, and responses are compared to the reference response.
- Error Message Detection: Responses are compared with known error messages in the `errors.txt` file to identify SQL injection vulnerabilities.
- Response Variation Analysis: If differences are detected in the content or header metadata of the responses, this is flagged as a potential SQL injection.
- Parallel Processing with ThreadPoolExecutor: Multiple requests are sent concurrently to speed up the testing process.

Requirements
- Python 3.x
- requests library (Installation: `pip install requests`)

Installation and Usage
- Adding SQL Payloads: Update the `sorgu.txt` file with one payload per line.
- Adding Error Messages: Add known error messages to the `errors.txt` file, one message per line.
- Adding User Agents: Include user agents in the `user-agents.txt` file.

Running from Command Line
You can run the tool using the following command:
python main.py -g <TARGET_URL> [-p] [-d <POST_DATA>] [-c <CONFIG_FILE>]


Parameters
- `-g, --url` (required): Target URL.
- `-p, --post`: Used for POST requests (default is GET).
- `-d, --data`: Parameters to send as POST data, e.g., `username=test&password=test`.
- `-c, --config`: Configuration file (optional).

Example Usage
python main.py -g http://example.com/page?id=

This command tests the specified URL for SQL injection vulnerabilities using payloads from the `sorgu.txt` file and error messages from the `errors.txt` file.
