import requests
import time
import os
from fake_useragent import UserAgent

class Appmus:
    def __init__(self):
        self.api = requests.Session()
        self.ua = UserAgent().random

    def read_cookie(self, cookie_file):
        with open(cookie_file, 'r') as cookie_file:
            return cookie_file.read().strip()

    def check_valid(self, code, cookie_file):
        cookie = self.read_cookie(cookie_file)

        headers = {
            'User-Agent': self.ua,
            'Content-Type': 'application/json',
            'Connection': 'keep-alive',
            'Cookie': cookie,
            'X-Apple-Store-Front': '143476-37,8'
        }

        params = {
            'code': code,
            'adamId': '',
            'bundleId': 'music'
        }

        resp = self.api.get('https://buy.music.apple.com/commerce/web/redeemInfo', headers=headers, params=params)

        if 'true' in resp.text:
            data = resp.json()
            code = data['codeSalableInfo']['code']
            offer = data['offerDetails']['offerDuration']
            exp = data['expDate']
            print(f'[+] Live: [{code}], Offer: [{offer}], Exp: [{exp}]')
            with open('applemusicvalid.txt', 'a') as file:
                file.write(f'[+] Live: [{code}], Offer: [{offer}], Exp: [{exp}]' + '\n')
        elif resp.status_code == 429:
            print(f'[!] Rate limit exceeded. ')
            time.sleep(50)
            self.check_valid(code, cookie_file)
        elif 'authentication' in resp.text:
            print('[!] Cookie Bad!')

if __name__ == "__main__":
    bot = Appmus()
    os.system('cls')
    print('<[Apple Music Code Checker]>')
    cookie_file = input('[!] Cookie File: ')
    file_path = input('[+] List: ')

    with open(file_path, 'r') as file:
        for code in file:
            bot.check_valid(code.strip(), cookie_file)
            time.sleep(5)
