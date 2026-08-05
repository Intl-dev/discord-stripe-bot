import os
import fastapi
import httpx
import dotenv

dotenv.load_dotenv()
discord_webhook = os.getenv('DISCORD_WEBHOOK')
app = fastapi.FastAPI()

@app.post("/webhook")
async def webhook(payload: dict):
    """Receives the json from fake-client.py, creates an embed with its info and sends it to the discord webhook"""
    amount = payload['data']['object']['amount'] / 100 #the amound is in cents so we convert it
    discord_payload = {
        "username": "Spidey Bot",
        "embeds": [
            {
                "title": f"Payment {payload['data']['object']['description']}",
                "description": "A (test) payment from stripe has been done",
                "color": 3447003,
                "fields": [
                    {"name": "Payment ID", "value": f"{payload['data']['object']['id']}", "inline": True},
                    {"name": "email", "value": f"{payload['data']['object']['receipt_email']}", "inline": True},
                    {"name": "status", "value": f"{payload['data']['object']['status']}", "inline": True},
                    {"name": "amount", "value": f"{amount},{payload['data']['object']['currency']}", "inline": True}
                ],
            }
        ],
    }
    async with httpx.AsyncClient() as client:
        discord_request = await client.post(discord_webhook, json=discord_payload)
        print(discord_request.status_code)

if __name__ == "__main__":
    #opens the port to receive the request from fake-client.py
    import uvicorn
    uvicorn.run("discord-webhook:app", host="127.0.0.1", port=8000, reload=True)