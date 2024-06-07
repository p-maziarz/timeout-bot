import discord
from discord.ext import commands
import asyncio

TOKEN = 'ENTER API KEY HERE'
PREFIX = '!'  # Change this to your desired bot prefix

# Define intents
intents = discord.Intents.default()
intents.presences = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# Dictionary to store user timeouts
timeouts = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def timeout(ctx, member: discord.Member, duration: int):
    timeouts[member.id] = duration
    await ctx.send(f'{member.display_name} has been timed out for {duration} seconds.')
    await asyncio.sleep(duration)
    del timeouts[member.id]
    await ctx.send(f'{member.display_name} has been untimed out.')

@bot.event
async def on_message(message):
    # Check if the author of the message is timed out
    if message.author.id in timeouts:
        await message.delete()
        await message.author.send("You're currently timed out and cannot send messages.")
    else:
        await bot.process_commands(message)

bot.run(TOKEN)
