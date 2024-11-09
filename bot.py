import os
import aiohttp
import discord
import ssl
import random
from discord import app_commands
from discord.ext import commands
from json import loads
from pathlib import Path
from webserver import keep_alive
from os import environ
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.message_content = True
intents.members = True

load_dotenv()

TOKEN = environ["TOKEN"]
bot = commands.Bot(command_prefix="!", intents=intents)  # Keep command_prefix as "!" to prevent initialization error

football_quotes = [
    "Success is no accident. It is hard work, perseverance, learning, studying, sacrifice and most of all, love of what you are doing or learning to do. - Pele",
    "The only place success comes before work is in the dictionary. - Vince Lombardi",
    "Winning isn’t everything, it’s the only thing. - Vince Lombardi",
    "The difference between ordinary and extraordinary is that little extra. - Jimmy Johnson",
    "It's not whether you get knocked down, it's whether you get up. - Vince Lombardi",
    "Perfection is not attainable, but if we chase perfection we can catch excellence. - Vince Lombardi",
    "The harder you work, the harder it is to surrender. - Marv Levy",
    "Football is like life - it requires perseverance, self-denial, hard work, sacrifice, dedication and respect for authority. - Vince Lombardi",
    "The road to Easy Street goes through the sewer. - John Madden",
    "If you want to win, do the ordinary things better than anyone else does them day in and day out. - Chuck Noll"
]


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()  # Syncs slash commands with Discord
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Error syncing commands: {e}")

@bot.tree.command(name="team", description="Displays information about the Uni Wien Emperors Team")
async def team_info(interaction: discord.Interaction):
    await interaction.response.send_message(
        "🏈 Welcome to the Uni Wien Emperors Discord! We are the University of Vienna's American Football Team. Let's dominate the field! 🏆"
    )

@bot.tree.command(name="schedule", description="Displays the Uni Wien Emperors Season Schedule")
async def schedule(interaction: discord.Interaction):
    schedule_text = (
        "📅 **Uni Wien Emperors Season Schedule** 📅\n\n"
        "🏈 **End of April** - VS. MUW Serpents\n"
        "    *ACSL Football Gameday 3 - Stadium TBA*\n\n"
        "🏈 **May 4, 2025** - VS. JKU Astros\n"
        "    *JKU Astros Football Gameday in Linz - ABC Platz*\n\n"
        "🏈 **Mid-May** - VS. TU Robots\n"
        "    *ACSL Football Gameday 5 - Stadium TBA*\n\n"
        "🏈 **Early June** - Semifinals\n"
        "    *Stadium TBA*\n\n"
        "🏆 **End of June** - Summer Bowl\n"
        "    *Stadium TBA*\n\n"
        "Sei dabei and support the Uni Wien Emperors! 🦅👑")
    await interaction.response.send_message(schedule_text)

@bot.tree.command(name="motivation", description="Get a motivational message to keep you going")
async def motivation(interaction: discord.Interaction):
    await interaction.response.send_message(
        "💪 Remember, Emperors, champions are made not just on the field, but in every workout, every practice, every day. Let's bring that Emperor spirit! 🏈🔥"
    )

@bot.tree.command(name="random", description="Get a random motivational quote")
async def motivation(interaction: discord.Interaction):
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.quotable.io/random', ssl=ssl_context) as response:
            if response.status == 200:
                data = await response.json()
                quote = data['content']
                author = data['author']
                await interaction.response.send_message(f"💪 {quote} - {author} 🏈🔥")
            else:
                await interaction.response.send_message("💪 Couldn't fetch a motivational quote at the moment. Please try again later. 🏈🔥")

@bot.tree.command(name="football", description="Get a motivational football quote")
async def random_quote(interaction: discord.Interaction):
    quote = random.choice(football_quotes)
    await interaction.response.send_message(f"💪 {quote} 🏈🔥")


@bot.tree.command(name="sync", description="Syncs commands with Discord")
async def sync_commands(interaction: discord.Interaction):
    synced = await bot.tree.sync()
    await interaction.response.send_message(f"Synced {len(synced)} commands.")

keep_alive()
bot.run(TOKEN)
