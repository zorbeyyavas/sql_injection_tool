import urllib.parse
import logging

def load_payloads(file_path):
    try:
        with open(file_path, 'r') as file:
            payloads = [line.strip() for line in file.readlines()]
        logging.info("Payload'lar başarıyla yüklendi.")
        return payloads
    except Exception as e:
        logging.error(f"Payload dosyası yüklenirken hata: {e}")
        return []

def obfuscate_payloads(payload):
    obfuscations = [
        urllib.parse.quote(payload),
        "".join([f"%{hex(ord(c))[2:]}" for c in payload]),
        "||".join(payload.split(" ")),
        payload.replace(" ", "/**/"),
        payload + "--",
        "/**/".join(payload.split(" ")),
    ]
    if "UNION" in payload:
        obfuscations.append(payload.replace("UNION", "UNION/**/"))
    if "SELECT" in payload:
        obfuscations.append(payload.replace("SELECT", "SELECT/**/"))
    
    return obfuscations
