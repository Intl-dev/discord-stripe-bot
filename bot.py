#the libraries
import asyncio
import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from database import check_unpaid

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print("bot is ready")

@bot.tree.command(name="unpaid_users", description="check the users that haven't paid")
async def unpaid_users(interaction: discord.Interaction):
    users = await check_unpaid()
    await interaction.response.send_message(users)

if __name__ == "__main__":
    bot.run(TOKEN)

