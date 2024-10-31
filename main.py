import argparse
import logging
import config, payload, error, user_agent, sql_injection

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    parser = argparse.ArgumentParser(description='SQL Injection Tester')
    parser.add_argument('-g', '--url', required=True, help='Hedef URL')
    parser.add_argument('-p', '--post', action='store_true', help='POST isteklerini kullan')
    parser.add_argument('-d', '--data', type=str, help='POST verileri (örneğin: username=test&password=test)')
    parser.add_argument('-c', '--config', type=str, help='Konfigürasyon dosyası')
    args = parser.parse_args()

    config_data = config.load_config(args.config) if args.config else {}
    
    payload_file_path = config_data.get('payloads_file', '/home/kullaniciadi/Desktop/tool/sorgu.txt')
    error_file_path = config_data.get('errors_file', '/home/kullaniciadi/Desktop/tool/errors.txt')
    user_agent_file_path = '/home/kullaniciadi/Desktop/tool/user-agents.txt'

    payloads = payload.load_payloads(payload_file_path)
    error_messages = error.load_error_messages(error_file_path)
    user_agents = user_agent.load_user_agents(user_agent_file_path)

    post_data = {}
    if args.data:
        post_data = dict(item.split('=') for item in args.data.split('&'))

    sql_injection.test_sql_injection(args.url, payloads, error_messages, user_agents, is_post=args.post, data=post_data)

if __name__ == "__main__":
    main()
