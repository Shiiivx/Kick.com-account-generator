import httpx, sys, json
import imaplib
import email
import re
from bs4 import BeautifulSoup as bs

acc = json.load(open("config.json"))["gmail"]

# use cloudflare to forward all messages
def msg(receiver, username=acc["email"], password=acc["password"]):
    while True:
        mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)
        mail.login(username, password)
        mail.select("inbox")
        result, data = mail.search(None, f'(TO "{receiver}")')
        if data[0]:
            break
    
    num = data[0].split()[-1]
    result, data = mail.fetch(num, "(RFC822)")
    raw_email = data[0][1]
    msg = email.message_from_bytes(raw_email)
    
    p = r'\b\d{6}\b'
    for part in msg.walk():
        if part.get_content_type() == "text/plain":
            body = part.get_payload(decode=True).decode()
            codes = re.findall(p, body)
            if codes:
                mail.logout()
                return codes[0] 
        elif part.get_content_type() == "text/html":
            body = part.get_payload(decode=True).decode()
            soup = bs(body, "html.parser")
            text = soup.get_text()
            codes = re.findall(p, text)
            if codes:
                mail.logout()
                return codes[0]
    mail.logout()
    return None

