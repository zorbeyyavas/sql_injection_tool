import argparse
import logging
from config_loader import load_config
from payload_manager import load_payloads, load_error_messages, load_user_agents
from sqli_tester import test_sql_injection

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    parser = argparse.ArgumentParser(description='SQL Injection Tester')
    parser.add_argument('-g', '--url', required=True, help='Hedef URL')
    parser.add_argument('-p', '--post', action='store_true', help='POST isteklerini kullan')
    parser.add_argument('-d', '--data', type=str, help='POST verileri (örneğin: username=test&password=test)')
    parser.add_argument('-c', '--config', type=str, help='Konfigürasyon dosyası')
    args = parser.parse_args()

    config = load_config(args.config) if args.config else {}
    
    payload_file_path = config.get('payloads_file', 'sorgu.txt')
    error_file_path = config.get('errors_file', 'errors.txt')
    user_agent_file_path = 'user-agents.txt'

    payloads = load_payloads(payload_file_path)
    error_messages = load_error_messages(error_file_path)
    user_agents = load_user_agents(user_agent_file_path)

    if not payloads or not error_messages or not user_agents:
        logging.error("Gerekli dosyalar yüklenemedi, işlem yapılamıyor.")
        return

    post_data = {}
    if args.data:
        try:
            post_data = dict(item.split('=') for item in args.data.split('&'))
        except ValueError:
            logging.error("POST verileri hatalı formatta.")
            return

    test_sql_injection(args.url, payloads, error_messages, user_agents, is_post=args.post, data=post_data)

if __name__ == "__main__":
    main()
