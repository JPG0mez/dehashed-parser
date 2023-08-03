import json
import csv
import argparse
import requests

def fetch_data_from_dehashed(domain, email, api_key):
    url = f"https://api.dehashed.com/search?query=domain:{domain}&size=10000&page=1"
    headers = {
        'Accept': 'application/json'
    }
    auth = (email, api_key)

    response = requests.get(url, headers=headers, auth=auth)

    if response.status_code == 200:
        domain_name = domain.split('.')[0]
        with open(f'{domain_name}.json', 'w', encoding='utf-8') as f:
            f.write(response.text)
        return True
    else:
        print(f"Error: Unable to fetch data from Dehashed API. Status Code: {response.status_code}")
        return False

def process_data(json_file, domain):
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: File not found.")
        return
    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")
        return
    if data.get('entries') is None:
        print(f"Error: No data found for domain '{domain}'.")
        return

    domain_name = domain.split('.')[0]
    passw_file = f'{domain_name}.passw'
    hashes_file = f'{domain_name}.hashes'

    passw_set = set()  # To store unique email-password pairs
    hashes_set = set()  # To store unique email-hash pairs

    for entry in data.get('entries', []):
        email = entry.get('email', '')
        password = entry.get('password', '')
        hashed_password = entry.get('hashed_password', '')

        if email and password and f"{email}:{password}" not in passw_set and password not in {"xxx", "temp"}:
            passw_set.add(f"{email}:{password}")

            passw_set.add(f"{email}:{password}")

        if email and hashed_password and f"{email}:{hashed_password}" not in hashes_set and hashed_password not in {"xxx", "temp"}:
            hashes_set.add(f"{email}:{hashed_password}")

    with open(passw_file, 'w', newline='', encoding="utf-8") as passwfile, \
            open(hashes_file, 'w', newline='', encoding="utf-8") as hashesfile:

        passw_writer = csv.writer(passwfile)
        hashes_writer = csv.writer(hashesfile)

        passw_writer.writerow(["email", "value"])
        hashes_writer.writerow(["email", "value"])

        for email_pass in passw_set:
            email, password = email_pass.split(':', 1)
            passw_writer.writerow([f"{email}:{password}"])

        for email_hash in hashes_set:
            email, hashed_password = email_hash.split(':', 1)
            hashes_writer.writerow([f"{email}:{hashed_password}"])
    num_passwords_found = len(passw_set)
    num_hashes_found = len(hashes_set)
    balance = data.get('balance', 0)

    print(f"Number of passwords found: {num_passwords_found}")
    print(f"Number of hashes found: {num_hashes_found}")
    print(f"Balance remaining: {balance}")
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetches and parses data from Dehashed API')
    parser.add_argument('domain', type=str, help='Domain to fetch data for')
    parser.add_argument('email', type=str, help='Your email for authentication')
    parser.add_argument('api_key', type=str, help='Your API key for authentication')
    args = parser.parse_args()

    if fetch_data_from_dehashed(args.domain, args.email, args.api_key):
        domain_name = args.domain.split('.')[0]
        process_data(f'{domain_name}.json', args.domain)
