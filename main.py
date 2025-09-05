import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import json
import os
import asyncio

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise RuntimeError("❌ DISCORD_TOKEN not found. Add it in Railway Variables.")

GAMES_FILE = "games.json"

# Load games
if os.path.exists(GAMES_FILE):
    with open(GAMES_FILE, "r") as f:
        try:
            games = json.load(f)
        except json.JSONDecodeError:
            games = {}
else:
    games = {}

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    await bot.tree.sync()
    print("🔧 Synced commands globally")

@bot.tree.command(name="addgame", description="Upload a zip game file (admin only)")
@app_commands.checks.has_permissions(administrator=True)
async def addgame(interaction: discord.Interaction, file: discord.Attachment):
    await interaction.response.defer(thinking=True)

    if not file.filename.endswith(".zip"):
        await interaction.followup.send("❌ Please upload a `.zip` file.")
        return

    os.makedirs("games", exist_ok=True)
    save_path = os.path.join("games", file.filename)

    # Download file from Discord to our server
    async with aiohttp.ClientSession() as session:
        async with session.get(file.url) as resp:
            if resp.status != 200:
                await interaction.followup.send("❌ Failed to download file.")
                return
            with open(save_path, "wb") as f:
                f.write(await resp.read())

    # Save game ID (name without .zip)
    game_id = file.filename.replace(".zip", "")
    games[game_id] = f"/{file.filename}"
    with open(GAMES_FILE, "w") as f:
        json.dump(games, f, indent=4)

    await interaction.followup.send(f"✅ Added `{game_id}` → {file.filename}")

@bot.tree.command(name="give", description="Get the download link for a game")
@app_commands.describe(game_id="The ID of the game to get")
async def give(interaction: discord.Interaction, game_id: str):
    if game_id not in games:
        await interaction.response.send_message(f"❌ No game found with ID `{game_id}`")
    else:
        base_url = os.getenv("RAILWAY_URL", "http://localhost:8080")
        await interaction.response.send_message(
            f"🎮 `{game_id}` → {base_url}{games[game_id]}"
        )

bot.run(TOKEN)

