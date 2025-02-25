import requests, json

config = json.load(open("config.json"))["imap"]
def createEmail(apiURL, email, password): # you better keep the passwords of all the accounts here same to access them later easily
    # apiURL: your API URL you have set up (https://github.com/Bluyx/email-api)
    # email: the email you want to create
    # password: the password for the email
    return requests.post(f"{apiURL}/create_email", data={"email": email, "password": password}).json()
def getVerification(email, password, apiUrl=config["apiUrl"], imap=config["imap"], sender="noreply@email.kick.com", verification_location="body"):
    # email: the email used in createEmail
    # password: the password used in createEmail
    # apiURL: your API URL you have set up (https://github.com/Bluyx/email-api)
    # imap: your imap domain, for example "mail.example.com"
    # sender: the email that sent the verification message, for example "noreply@email.kick.com" (you can set it to "ALL")
    # verification_location: the location of the verification ["subject", "body"]
    return requests.post(f"{apiUrl}/get_verification", data = {
        "email": email,
        "password": password,
        "sender": sender,
        "verification_location": verification_location,
        "imap": imap
    }).json()




