import requests
import random


WEBHOOK_URL = "http://127.0.0.1:8000/webhook"


def generate_fake_payment():
    amounts = [1500, 2999, 4900, 9900]
    emails = ["john.doe@gmail.com", "jane.smith@yahoo.com", "alex_dev@hotmail.com"]

    chosen_amount = random.choice(amounts)
    chosen_email = random.choice(emails)
    payment_id = f"pi_test_{random.randint(100000, 999999)}"


    payload = {
        "id": f"evt_test_{random.randint(1000, 9999)}",
        "type": "payment_intent.succeeded",
        "data": {
            "object": {
                "id": payment_id,
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
    payment = generate_fake_payment()
    response = requests.post(WEBHOOK_URL, json=payment)
    if response.status_code == 200:
        print(response.json())
    else:
        print(response.status_code)
