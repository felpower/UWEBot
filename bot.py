import os
import aiohttp
import discord
from discord import app_commands
from discord.ext import commands

from webserver import keep_alive

intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.message_content = True
intents.members = True

TOKEN = "MTMwNDQzNDk2Nzc5OTE0MDM3NA.GQG4-8.lB_nmOzFtST_k92jHMJzlkEzhZZjZiOJ-m4G6I"

bot = commands.Bot(command_prefix="!", intents=intents)  # Keep command_prefix as "!" to prevent initialization error

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()  # Syncs slash commands with Discord
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Error syncing commands: {e}")

@bot.tree.command(name="team")
async def team_info(interaction: discord.Interaction):
    await interaction.response.send_message(
        "🏈 Welcome to the Uni Wien Emperors Discord! We are the University of Vienna's American Football Team. Let's dominate the field! 🏆"
    )

@bot.tree.command(name="schedule")
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

@bot.tree.command(name="motivation")
async def motivation(interaction: discord.Interaction):
    await interaction.response.send_message(
        "💪 Remember, Emperors, champions are made not just on the field, but in every workout, every practice, every day. Let's bring that Emperor spirit! 🏈🔥"
    )

@bot.tree.command(name="random")
async def motivation(interaction: discord.Interaction):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.quotable.io/random') as response:
            if response.status == 200:
                data = await response.json()
                quote = data['content']
                author = data['author']
                await interaction.response.send_message(f"💪 {quote} - {author} 🏈🔥")
            else:
                await interaction.response.send_message("💪 Couldn't fetch a motivational quote at the moment. Please try again later. 🏈🔥")


@bot.tree.command(name="sync")
async def sync_commands(interaction: discord.Interaction):
    synced = await bot.tree.sync()
    await interaction.response.send_message(f"Synced {len(synced)} commands.")

keep_alive()
bot.run(TOKEN)
