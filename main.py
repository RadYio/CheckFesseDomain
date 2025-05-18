import whois
import time
import requests
import os

DOMAIN_NAME = os.environ.get("DOMAIN_NAME", "google.com")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", print("Please set the TELEGRAM_TOKEN environment variable."))
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", print("Please set the TELEGRAM_CHAT_ID environment variable."))

CHECK_INTERVAL = 86400  / 2 # 24h / 2 = 12h

last_expiry = None
last_status = None

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, data=data)

def check_domain():
    global last_expiry, last_status
    try:
        w = whois.whois(DOMAIN_NAME)
        expiry = str(w.expiration_date)
        status = str(w.status)

        if last_expiry != expiry or last_status != status:
            message = f"🔍 Changement détecté sur {DOMAIN_NAME} :\n"
            if last_expiry != expiry:
                message += f"⏰ Nouvelle expiration : {expiry}\n"
            if last_status != status:
                message += f"📌 Nouveau statut : {status}\n"
            send_telegram(message)
            print(message)
            last_expiry = expiry
            last_status = status
        else:
            message = f"✅ Pas de changement sur {DOMAIN_NAME} :\nExpiration : {expiry}\nStatut : {status}"
            print(message)
            send_telegram(message)
            

    except Exception as e:
        send_telegram(f"⚠️ Erreur lors de la vérification : {e}")

if __name__ == "__main__":
    print(f"🔍 Vérification de {DOMAIN_NAME} toutes les {CHECK_INTERVAL / 3600} heures...")
    while True:
        check_domain()
        time.sleep(CHECK_INTERVAL)
