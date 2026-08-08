import os
import fastapi
import httpx
import dotenv
from database import insert_invoice

dotenv.load_dotenv()
discord_webhook = os.getenv('DISCORD_WEBHOOK')
app = fastapi.FastAPI()

@app.post("/webhook")
async def webhook(payload: dict):
    """Receives the json from fake-client.py, creates an embed with its info and sends it to the discord webhook"""
    user_id = payload["data"]["object"]["discord_id"]
    payment_id = payload["data"]["object"]["payment_id"]
    payment_url = payload["data"]["object"]["payment_url"]
    email = payload["data"]["object"]["receipt_email"]
    if payload["data"]["object"]["status"] == "succeeded":
        status = "PAID"
    else:
        status = payload["data"]["object"]["status"]

    amount = payload['data']['object']['amount'] / 100 #the amount is in cents so we convert it
    currency = payload['data']['object']['currency']
    discord_payload = {
        "username": "Spidey Bot",
        "embeds": [
            {
                "title": f"Payment {payload['data']['object']['description']}",
                "description": "A (test) payment from stripe has been done",
                "color": 3447003,
                "fields": [
                    {"name": "User ID", "value": f"{user_id}", "inline": True},
                    {"name": "Payment ID", "value": f"{payment_id}", "inline": True},
                    {"name": "Payment URL", "value": f"{payment_url}", "inline": True},
                    {"name": "email", "value": f"{email}", "inline": True},
                    {"name": "status", "value": f"{status}", "inline": True},
                    {"name": "amount", "value": f"{amount},{currency}", "inline": True}
                ],
            }
        ],
    }
    await insert_invoice(str(payment_id), int(user_id), float(amount), str(payment_url), str(status))
    async with httpx.AsyncClient() as client:
        discord_request = await client.post(discord_webhook, json=discord_payload)
        print(discord_request.status_code)


if __name__ == "__main__":
    #opens the port to receive the request from fake-client.py
    import uvicorn
    uvicorn.run("discord-webhook:app", host="127.0.0.1", port=8000)
