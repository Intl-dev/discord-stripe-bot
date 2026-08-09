import requests
import random
import os
import dotenv
dotenv.load_dotenv()
discord_id = os.getenv("DISCORD_ID")
#this is basically my pc
WEBHOOK_URL = "http://127.0.0.1:8000/webhook"

def generate_fake_payment():
    """Creates a test json for the local server (AKA my pc) to process it"""
    amounts = [1500, 2999, 4900, 9900]
    emails = ["john.doe@gmail.com", "jane.doe@yahoo.com", "builderman@hotmail.com"]
    chosen_amount = random.choice(amounts)
    chosen_email = random.choice(emails)
    payment_id = f"pi_test_{random.randint(100000, 999999)}"
    payment_url = f"http://127.0.0.1:8000/payment/{payment_id}"

    #this is a fake stripe payment for tests
    payload = {
        "id": f"evt_test_{random.randint(1000, 9999)}",
        "type": "payment_intent.succeeded",
        "data": {
            "object": {
                "discord_id": discord_id,
                "payment_id": payment_id,
                "payment_url": payment_url,
                "amount": chosen_amount,
                "currency": "usd",
                "status": "succeeded",
                "receipt_email": chosen_email,
                "description": "Pro Plan Subscription"
            }
        }
    }
    return payload

if __name__ == "__main__":
    #Sends the json
    payment = generate_fake_payment()
    response = requests.post(WEBHOOK_URL, json=payment)
    if response.status_code == 200:
        print("it's working")
    else:
        print(response.status_code)
