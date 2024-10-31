import requests
import logging

def get_response(url, headers, method='GET', data=None):
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers, timeout=5)
        elif method == 'POST':
            response = requests.post(url, headers=headers, data=data, timeout=5)
        return response
    except requests.Timeout:
        logging.error("Zaman aşımına uğradı.")
        return None
    except requests.ConnectionError:
        logging.error("Bağlantı hatası.")
        return None
    except requests.RequestException as e:
        logging.error(f"İstek sırasında hata: {e}")
        return None
