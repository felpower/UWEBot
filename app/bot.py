import discord
import ssl
import random
import instaloader
from discord.ext import commands, tasks
from webserver import keep_alive
from os import environ
from dotenv import load_dotenv
import concurrent.futures
import asyncio

intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.message_content = True
intents.members = True

load_dotenv()

TOKEN = environ["TOKEN"]
INSTAGRAM_USERNAME = environ["INSTAGRAM_USERNAME"]

bot = commands.Bot(command_prefix="!", intents=intents)  # Keep command_prefix as "!" to prevent initialization error

last_post_id = None

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

@bot.tree.command(name="orga", description="Who is responsible for what in the organization?")
async def motivation(interaction: discord.Interaction):
    await interaction.response.send_message(
        '''💪 Präsident:
Jimmy und Johann (Co.)
Hauptverantwortung für die Leitung und Koordination des Teams.

Finanzen:
Verantwortlicher: Patrick Sommerauer
Jahresbericht und Jahresvoranschlag erstellen.
Einzahlungen und Auszahlungen überprüfen und tätigen.
SEPA-Lastschriften erstellen und austeilen.

Coaching:
Verantwortlicher: Flo Sikora
Helfer: Stefan Gamperl
Trainingspläne erstellen und Coaches organisieren.
Hudl-Management und Teilnahme an ACSL-Sitzungen.

Administration:
Verantwortlicher: Noch offen (???)
Förderungen erschließen.
Weihnachtsfeier organisieren.
Stadlauer Kontakt pflegen und Vertragsverlängerungen bearbeiten.
Spielerpässe überprüfen und Raumbuchungen in Stadlau organisieren.

Sportliche Leitung:
Verantwortlicher: Lukas Steiner
Camps planen und buchen.
Tryouts organisieren.
Rookie-Leitfaden erstellen und aktualisieren.
Testspiele organisieren.
Coaching-Qualitätsüberwachung (Feedbackbögen erstellen, auswerten und Rückmeldung geben).

Equipment:
Verantwortlicher: Noch offen (???)
Gameday-Organisation.
Inventar überprüfen und Equipment bestellen.
Jersey-Vergabe und -Überwachung.
Jersey-Bestellungen planen.
Equipment überprüfen und pflegen, inklusive Transportplanung.

Social Media:
Verantwortlicher: Martin
Beiträge erstellen und Informationen nach außen kommunizieren.
Instagram-Anfragen beantworten.
Media-Days planen.

Allgemeines:
Verantwortlicher: Jimmy
Erstellung des Jahresberichts und Jahresvoranschlags (zusammen mit anderen Bereichen).
Unterstützung bei der Planung von Camps und Buchungen. 🏈🔥'''
    )

@bot.tree.command(name="football", description="Get a motivational football quote")
async def random_quote(interaction: discord.Interaction):
    quote = random.choice(football_quotes)
    await interaction.response.send_message(f"💪 {quote} 🏈🔥")

# @tasks.loop(minutes=15)  # Checks every 15 minutes
# async def check_instagram():
#     print("Checking Instagram...")
#     global last_post_id
#     channel = bot.get_channel(1302669836282888222)  # Replace with your channel ID

#     def fetch_instagram_posts():
#         try:
#             loader = instaloader.Instaloader()
#             loader.load_session_from_file(INSTAGRAM_USERNAME)
#             profile = instaloader.Profile.from_username(loader.context, "uniwienemperors")  # Username of the account
#             posts = [post for post in profile.get_posts() if not post.is_pinned]
#             return posts
#         except Exception as e:
#             print(f"Error fetching Instagram data: {e}")
#             return None

#     loop = asyncio.get_event_loop()
#     with concurrent.futures.ThreadPoolExecutor() as pool:
#         posts = await loop.run_in_executor(pool, fetch_instagram_posts)

#     if posts:
#         latest_post = posts[0] if posts else None
#         if latest_post and (last_post_id is None or latest_post.shortcode != last_post_id):
#             last_post_id = latest_post.shortcode
#             post_url = f"https://www.instagram.com/p/{latest_post.shortcode}/"
#             print(f"New Instagram post: {post_url}")
#             await channel.send(f"📸 New Instagram Post!\n{post_url}")

@bot.tree.command(name="sync", description="Syncs commands with Discord")
async def sync_commands(interaction: discord.Interaction):
    synced = await bot.tree.sync()
    await interaction.response.send_message(f"Synced {len(synced)} commands.")

keep_alive()
bot.run(TOKEN)