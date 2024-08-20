import requests
import time
import sys
from colorama import Fore, init

init(autoreset=True)

# Langkah 1: Mendapatkan access_token dan menyimpannya ke sesi.txt
def get_access_tokens():
    access_tokens = []
    with open('query.txt', 'r') as file:
        x_tg_data_list = [line.strip() for line in file if line.strip()]

    for x_tg_data in x_tg_data_list:
        url = "https://cowtopia-be.tonfarmer.com/auth"
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Content-Type": "application/json",
            "Origin": "https://cowtopia-prod.tonfarmer.com",
            "Referer": "https://cowtopia-prod.tonfarmer.com/",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, seperti Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
            "X-Chain-Id": "43113",
            "X-Lang": "en",
            "X-Os": "miniapp",
            "X-Tg-Data": x_tg_data,
        }

        payload = {}
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 201:
            data = response.json()
            access_token = data['data']['access_token']
            access_tokens.append(access_token)
            
        else:
            print(f"Gagal mendapatkan token untuk akun: {x_tg_data}, status code: {response.status_code}")
    
    # Simpan semua token ke sesi.txt
    with open('sesi.txt', 'w') as file:
        for token in access_tokens:
            file.write(token + '\n')

# Langkah 2: Menggunakan access_token untuk mendapatkan informasi game dan klaim offline profit
def fetch_game_info(session):
    try:
        response = requests.get(
            "https://cowtopia-be.tonfarmer.com/user/game-info?",
            headers={
                "accept": "application/json, text/plain, */*",
                "accept-language": "en-US,en;q=0.9",
                "authorization": f"Bearer {session}",
                "if-none-match": "W/\"6af-iEg+sTAdCtXuNMD5aYzsYKpHHEA\"",
                "priority": "u=1, i",
                "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Microsoft Edge\";v=\"127\", \"Chromium\";v=\"127\", \"Microsoft Edge WebView2\";v=\"127\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"Windows\"",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-site",
                "x-chain-id": "43113",
                "x-lang": "en",
                "x-os": "miniapp",
                "referer": "https://cowtopia-prod.tonfarmer.com/"
            }
        )
        response.raise_for_status()
        result = response.json()
        if result.get('success'):
            username = result['data']['user']['username']
            money = result['data']['user']['money']
            print(Fore.CYAN + f"Username: {username}, Money: {money}")
            return True
        else:
            print(Fore.RED + "Gagal mengambil informasi game.")
            return False
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Kesalahan dalam permintaan: {e}")
        return False
    except ValueError as e:
        print(Fore.RED + f"Kesalahan dalam parsing JSON: {e}")
        return False
    except Exception as e:
        print(Fore.RED + f"Terjadi kesalahan saat mengambil informasi game: {e}")
        return False

def claim_offline_profit(session):
    try:
        response = requests.get(
            "https://cowtopia-be.tonfarmer.com/user/offline-profit?",
            headers={
                "accept": "application/json, text/plain, */*",
                "accept-language": "en-US,en;q=0.9",
                "authorization": f"Bearer {session}",
                "if-none-match": "W/\"4d-8oYmJt67vgrL0CPXBLSRb8WrZ/Q\"",
                "priority": "u=1, i",
                "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Microsoft Edge\";v=\"127\", \"Chromium\";v=\"127\", \"Microsoft Edge WebView2\";v=\"127\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"Windows\"",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-site",
                "x-chain-id": "43113",
                "x-lang": "en",
                "x-os": "miniapp",
                "referer": "https://cowtopia-prod.tonfarmer.com/"
            }
        )
        response.raise_for_status()
        if response.text.strip():
            result = response.json()
            if result.get('success'):
                print(Fore.GREEN + f"Offline profit {result['data']['profit']} berhasil di claim.")
            else:
                print(Fore.RED + "Gagal mengklaim offline profit.")
        else:
            print(Fore.RED + "Respons kosong diterima.")
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Kesalahan dalam permintaan: {e}")
    except ValueError as e:
        print(Fore.RED + f"Kesalahan dalam parsing JSON: {e}")
    except Exception as e:
        print(Fore.RED + f"Terjadi kesalahan saat klaim offline profit: {e}")

def countdown(minutes):
    for remaining in range(minutes * 60, 0, -1):
        mins, secs = divmod(remaining, 60)
        timeformat = f'{mins:02}:{secs:02}'
        sys.stdout.write(Fore.YELLOW + f"\rMenunggu {minutes} menit lagi: {timeformat}")
        sys.stdout.flush()
        time.sleep(1)
    print()

# Main script
try:
    get_access_tokens()
    with open('sesi.txt', 'r') as file:
        sessions = [line.strip() for line in file if line.strip()]

    while True:
        for session in sessions:
            if fetch_game_info(session):
                claim_offline_profit(session)
                time.sleep(5)
        print(Fore.CYAN + "Semua sesi selesai. Menunggu 5 menit sebelum memulai ulang...")
        countdown(5)
except KeyboardInterrupt:
    print(Fore.RED + "\nProses dihentikan oleh pengguna.")
