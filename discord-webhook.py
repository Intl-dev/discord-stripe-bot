
import os
import fastapi

discord_webhook = os.getenv('DISCORD_WEBHOOK')
app = fastapi.FastAPI()
@app.post("/webhook")
async def webhook(payload: dict):
    print(payload)

