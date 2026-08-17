import os
import fastapi
import httpx
import dotenv
from database import insert_invoice


dotenv.load_dotenv()
discord_webhook = os.getenv('DISCORD_WEBHOOK')
discord_id = os.getenv('DISCORD_ID')
guild_id = os.getenv('GUILD_ID')
role_id = os.getenv('ROLE_ID')
bot_token = os.getenv('BOT_TOKEN')
app = fastapi.FastAPI()

@app.post("/webhook")
async def webhook(response: dict):
    """Receives the json from fake-client.py, creates an embed with its info and sends it to the discord webhook"""
    customer = response["customer"]
    status = response["status"]
    payment_url = None
    order_id = customer["metadata"]["order_id"]
    email = customer["email"]
    amount = customer["balance"] / 100 #the amount is in cents so we convert it
    currency = customer["currency"]
    description = customer["description"]
    customer_id = customer["id"]

    discord_payload = {
        "username": "Spidey Bot",
        "embeds": [
            {
                "title": f"Payment {description}",
                "description": "A (test) payment from stripe has been done",
                "color": 3447003,
                "fields": [
                    {"name": "User ID", "value": f"{customer_id}", "inline": True},
                    {"name": "Payment ID", "value": f"{order_id}", "inline": True},
                    {"name": "Payment URL", "value": f"{payment_url}", "inline": True},
                    {"name": "email", "value": f"{email}", "inline": True},
                    {"name": "status", "value": f"{status}", "inline": True},
                    {"name": "amount", "value": f"{amount},{currency}", "inline": True}
                ],
            }
        ],
    }
    await insert_invoice(str(order_id), str(customer_id), float(amount), str(payment_url), str(status))

    async def assign_role(discord_id: int, status: str):
        if status == "PAID":
            url = f"https://discord.com/api/v10/guilds/{guild_id}/members/{discord_id}/roles/{role_id}"
            auth = {"Authorization": f"Bot {bot_token}"}
            async with httpx.AsyncClient() as client:
                assign_response = await client.put(url, headers=auth)
                print(f"role assigment{assign_response.status_code}")
        else:
            print("cannot assign role")

    async def send_dm(discord_id: int):
        if status == "PAID":
            headers = {"Authorization": f"Bot {bot_token}"}
            text = f"You have been assigned the role of VIP"
            async with httpx.AsyncClient() as client:
                channel = await client.post("https://discord.com/api/v10/users/@me/channels", headers=headers, json={"recipient_id": str(discord_id)})
                msg = await client.post(f"https://discord.com/api/v10/channels/{channel.json()['id']}/messages", headers=headers, json={"content": text})
                print(f"message status code: {msg.status_code}")


        else:
            headers = {"Authorization": f"Bot {bot_token}"}
            text = f"Your payment failed, your VIP role has not been assigned"
            async with httpx.AsyncClient() as client:
                channel = await client.post("https://discord.com/api/v10/users/@me/channels", headers=headers,
                                            json={"recipient_id": str(user_id)})
                msg = await client.post(f"https://discord.com/api/v10/channels/{channel.json()['id']}/messages",
                                        headers=headers, json={"content": text})
                print(f"message status code: {msg.status_code}")

    await send_dm(discord_id)
    await assign_role(discord_id, status)


    async with httpx.AsyncClient() as client:
        discord_request = await client.post(discord_webhook, json=discord_payload)
        print(discord_request.status_code)


if __name__ == "__main__":
    #opens the port to receive the request from fake-client.py
    import uvicorn
    uvicorn.run("discord-webhook:app", host="127.0.0.1", port=8000)
