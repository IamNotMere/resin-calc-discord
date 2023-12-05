import asyncio
import discord
from discord.ext import commands
import sqlite3
import time
from keys import T

timetillfull = 0
max_resin_time = 0
response = None
data = None

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def sresin(ctx):
    global response, timetillfull, max_resin_time
    await ctx.send("Please provide your input. You have 10 seconds to respond.")

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    try:
        response_message = await bot.wait_for('message', check=check, timeout=10)
        response = response_message.content
        await ctx.send('Your input is: ' + response)

        if response is not None:
            conn = sqlite3.connect("discord.db")
            cursor = conn.cursor()

            # Create a Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    Resin INTEGER NOT NULL
                )
            ''')
            conn.commit()

            # Insert Data
            cursor.execute('''
                INSERT INTO users (Resin) VALUES (?)''', (response,))
            cursor.execute('''SELECT Resin FROM users''')
            data = cursor.fetchone()

            if data is not None and int(data[0]) <= 160:
                resintime = 0
                resintillfull = 160 - int(data[0])
                timetillfull = resintillfull * 8 * 60
                resintime += timetillfull
                max_resin_time = time.time() + resintime

    except asyncio.TimeoutError:
        await ctx.send('You did not respond in time.')

@bot.command()
async def genshin(ctx):
    global timetillfull, max_resin_time
    if timetillfull >= 76800:
        embed_description = 'Your resin is currently capped'
    else:
        embed_description = f'Your resin will be capped <t:{round(max_resin_time)}:R>'

    embed = discord.Embed(
        title='Genshin Resin',
        url='https://google.com',
        description=embed_description,
        color=0x440d5c
    )
    embed.set_author(
        name='Genshin Impact',
        icon_url='https://static.wikia.nocookie.net/gensin-impact/images/8/80/Genshin_Impact.png/revision/latest?cb=20230121174225'
    )
    await ctx.send(embed=embed)

@bot.command()
async def command(ctx):
    await ctx.send('''!

!genshin - check when your resin will cap.(Only use after using !sresin)
!sresin - Input how much resin you currently have''')

@bot.event
async def on_ready():
    print(f'{bot.user} is operational')

def run_discord_bot():
    bot.run(T().TOKEN1())
