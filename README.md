# Kick.com Account generator
Kick Account generator

## Features
- Email-Based Account Creation: With <a href="https://github.com/Bluyx/email-api">email api</a> You can Generate accounts using email addresses from your custom domain and receive the verification code automatically. (Use it like this: xxx@example.com) OR you can use <a href="https://kopeechka.store/?ref=28978">Kopeechka.store</a>
- Realistic usernames
- Customizable Options: Choose between realistic, random or specific usernames for each account and Choose whether to use random or specific passwords.

## Requirements
- Emails using <a href="https://kopeechka.store/?ref=28978">Kopeechka.store</a> or <a href="https://github.com/Bluyx/email-api">email api</a>
- <a href="https://salamoonder.com/">Salamoonder api key (Kasada Solver)</a>
- proxies

## Installation
```bash
git clone https://github.com/fqw3/Kick.com-account-generator
cd Kick.com-account-generator
pip install -r requirements.txt
```
Rename `config.json.example` to `config.json`<br>
Edit `config.json`<br>
If you want to use <a href="https://kopeechka.store/?ref=28978">Kopeechka.store</a> then put your token and the domains you want<br>
If you want to use <a href="https://github.com/Bluyx/email-api">Custom domain</a> then put your API URL, imap, emails domain 
```bash
python main.py
```

## Todo List
- Make it follow channels of the user's choice after each account is created
- Handle more errors
- Make the code more readable

## Contant
- Discord: <a href="https://discord.com/users/251794521908576257">2yv</a>
