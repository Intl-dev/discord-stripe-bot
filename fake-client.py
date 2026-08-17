import requests
import random
import os
import dotenv
from stripe import StripeClient

dotenv.load_dotenv()
discord_id = os.getenv("DISCORD_ID")
#this is basically my pc
WEBHOOK_URL = "http://127.0.0.1:8000/webhook"

def generate_fake_payment():
    """Creates a test JSON (with stripe integration) for the local server (AKA my pc) to process it"""

    client = StripeClient("sk_test_BQokikJOvBiI2HlWgH4olfQ2")
    customer = client.v1.customers.create({"metadata": {"order_id": "6735"}})
    status = "PAID" #this is a placeholder to have a status for the webhook
    return {"customer": customer.to_dict(),
            "status": status}

if __name__ == "__main__":
    #Sends the json
    payment = generate_fake_payment()
    response = requests.post(WEBHOOK_URL, json=payment)

    if response.status_code == 200:
        print("it's working")
    else:
        print(response.status_code)
