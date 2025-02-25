import random, json, websocket, time, os, time, bs4, sys, console, re
from kasada import salamoonder
import tls_client
import traceback
import requests
import json
import sys
import time
from kopeechka import getMail, getCode
from customDomain import msg
from mail import createEmail, getVerification
import random
import string
from datetime import datetime, timedelta

def random_string(length=5, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choices(chars, k=length))

def random_username():
    return f"{random_string(random.randint(7, 10), string.ascii_lowercase)}_{random_string(random.randint(7, 10), string.ascii_lowercase)}{random.randint(10, 9999)}"

def random_password():
    return ''.join(random.sample(
        random.choice(string.ascii_uppercase) + random.choice(string.ascii_lowercase) +
        random.choice(string.digits) + random.choice("!@#^") +
        ''.join(random.choices(string.ascii_letters + string.digits + "!@#^", k=8)), random.randint(8, 12)
    ))

def last_chrome_version():
    return requests.get("https://api.sockets.lol/browsers").json()["chrome"]
def hc(c):
    headersCookies = ""
    for name, value in c.cookies.items():
        headersCookies = headersCookies + f"{name}={value}; "
    return headersCookies[:-2]

config = json.load(open("config.json"))

def create_account(password=None, username=None, chromeVersion=last_chrome_version()):
    try:
        password = config["password"] if config["password"] else random_password()
        username = random_username()
        emailType = config["mailType"]
        if emailType == "kopeechka":
            email = getMail()
            email_id = email["id"]
            email = email["mail"]
        elif emailType == "imap":
            email = createEmail(config["imap"]["apiURL"], random_string(7), "password")
        elif emailType == "custom":
            email = random_string(random.randint(7,10)) + f"@{config["domain"]}"
            pass
        else:
            raise Exception("Unknown mailType (kopeechka|imap|custom)")
        console.info(f"Using {email} | Username {username}")
        proxy = random.choice(open("proxies.txt").readlines()).strip()
        client = tls_client.Session(client_identifier="chrome_120", random_tls_extension_order=True)
        client.proxies = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
        client.headers = {
            "user-agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chromeVersion}.0.0.0 Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9",
        }
        client.get("https://kick.com/")
        x = client.get("https://kick.com/sanctum/csrf")
        if x.status_code != 200:
            return create_account()
        xsrf = client.cookies["XSRF-TOKEN"].replace("%3D", "=")

        console.info(f"Got XSRF token")

        s = time.time()
        kasada = salamoonder()
        console.info(f"Solved kasada in {time.time()-s:.2f}s")
        client.headers.update({
            "authorization": f"Bearer {xsrf}",
            "x-xsrf-token": xsrf,
            "x-kpsdk-ct": kasada["x-kpsdk-ct"],
            "x-kpsdk-v": "j-0.0.0",
            "x-kpsdk-cd": kasada["x-kpsdk-cd"],
        })
        r = client.post("https://kick.com/api/v1/signup/send/email", json={"email": email})
        if r.status_code != 204:
            # create_account()
            return False
        s = time.time()
        console.info(f"Waiting for verification code...")
        if emailType == "kopeechka":
            code = getCode(email_id)
        elif emailType == "imap":
            code = getVerification(email, "password")
        else:
            code = msg(email)
            pass
        console.info(f"Got verification code {code} in {time.time()-s:.2f}s")
        r = client.post("https://kick.com/api/v1/signup/verify/code", json={"email": email, "code": code})
        if r.status_code != 204:
            # print(r.text)
            # print(r.status_code)
            return False
        ktp = client.get("https://kick.com/kick-token-provider").json()
        r = client.post('https://kick.com/register', json={
            "email": email,
            "birthdate": (datetime.today() - timedelta(days=365 * random.randint(18, 40))).strftime("%m/%d/%Y"),
            "username": username,
            "password": password,
            "newsletter_subscribed": False,
            ktp["nameFieldName"]: "",
            "_kick_token_valid_from": ktp["encryptedValidFrom"],
            "agreed_to_terms": True,
            "cf_captcha_token": "",
            "enable_sms_promo": False,
            "enable_sms_security": False,
            "password_confirmation": password,
            "isMobileRequest": True
        })
        if r.status_code != 200:
            print("Just a moment" in r.text)
            console.error(f"Failed to register: {r.status_code}")
            input()
            return create_account()
        token = r.json().get("token")
        if not token:
            console.error("Failed to register token")
            return False
        with open("kick_accounts.txt", "a") as f:
            f.write(f"{email}:{password}:{username}:{token}\n")
        return token
    except Exception:
        traceback.print_exc()
        return False

if __name__ == "__main__":
    start = time.time()
    email = f"{random_string(15, string.ascii_lowercase + string.digits)}@akszfjdw.cfd"
    token = create_account()
    if token:
        console.success(f"Created account {token} in {time.time()-start:.2f}s")


