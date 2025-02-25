import requests, sys, console, json

kop = json.load(open("config.json"))["kopeechka"]

def getMail(key=kop["key"], domain=kop["domains"]):
    req = requests.get(f"https://api.kopeechka.store/mailbox-get-email?site=kick.com&mail_type={domain}&token={key}&password=1&regex=&subject=&investor=&soft=&type=json&api=2.0", timeout=30).json()
    if req["status"] == "OK":
        return req
    elif req["status"] == "ERROR":
        if req["value"] == "BAD_TOKEN":
            sys.exit(console.error("Invalid kopeechka api key"))
        raise Exception(req["value"])

def getCode(id, key=kop["key"]):
    while True:
        req = requests.get(f"https://api.kopeechka.store/mailbox-get-message?full=1&id={id}&token={key}&type=json&api=2.0", timeout=30).json()
        if req["status"] == "OK":
            return req["fullmessage"]
        elif req["value"] == "WAIT_LINK":
            pass
        else: raise Exception(req["value"])



