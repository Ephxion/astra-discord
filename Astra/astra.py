import discord
from discord.ext import commands
from datetime import datetime
import requests
from aiohttp import request
import json
import googletrans
import random
from discord import Embed

token = open("notatoken.txt", "r")
TOKEN = token.read()
key = open("notakey.txt", "r")
KEY = key.read()
key2 = open("notaweb.txt", "r")
KEY2 = key2.read()
tgr = open("triggers.txt", "r")
TGR = tgr.readlines()
mah = open("maeh.txt", "r")
MAH = mah.readlines()
triggers = []
Maeh = []

for line in TGR:
    count = 0
    count += 1
    triggers.append(line.strip())

for line in MAH:
    count = 0
    count += 1
    Maeh.append(line.strip())

client = discord.Client()
client = commands.Bot(command_prefix=",")
is_client_running = False


@client.event
async def on_ready():
    global is_client_running
    print(f"Bot {client.user.name} initialising...")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(","):
        await message.channel.trigger_typing()

    await client.process_commands(message)

    if str(client.user.id) in message.content:
     await message.channel.send(f"{message.author.mention} Que me pingueas cara de pija")

@client.event
async def on_command_error(ctx, error):
    await ctx.send(error)
    print(datetime.now(), "command exception", type(error), error)


@client.command(aliases=['tgr', 'putear'])
async def trigger(ctx):
    await ctx.send(str(random.choice(triggers)))


@client.command(aliases=['Exit', 'exit', 'Exitao', 'Ephxion'])
async def nicolas(ctx):
    await ctx.send("https://media.discordapp.net/attachments/439986789902450689/817151763013435392/154570644_1762319797281712_2658469385935111180_o.png?width=676&height=676")    

@client.command(aliases=['maes', 'maestrulia', 'Maeh', 'Maehstrulia', 'Maes', 'maehstrulia',])
async def maeh(ctx):
    await ctx.send((str(random.choice(Maeh))))
    

@client.command()
@commands.dm_only()
@commands.is_owner()
async def say(ctx, *args):
    string_to_output = ' '.join(args)
    requests.post(KEY2, data=json.dumps({'content': string_to_output}), headers={'Content-type': 'application/json'})



@client.command()
async def wiki(ctx, *args):
    """
    Answers questions and queries using WolframAlpha's Simple API
    """

    query = '+'.join(args)
    url = f"https://api.wolframalpha.com/v1/result?appid={KEY}&i={query}%3F"
    response = requests.get(url)

    if response.status_code == 501:
        await ctx.send("No he podido encontrar informacion sobre eso.")
        return

    await ctx.send(response.text)

@client.command(aliases=['tr', 'traducir'])
async def translate(ctx, lang_to, *args):
    """
    Translates the given text to the language `lang_to`.
    The language translated from is automatically detected.
    """

    lang_to = lang_to.lower()
    if lang_to not in googletrans.LANGUAGES and lang_to not in googletrans.LANGCODES:
        raise commands.BadArgument("Invalid language to translate text to")

    text = ' '.join(args)
    translator = googletrans.Translator()
    text_translated = translator.translate(text, dest=lang_to).text
    await ctx.send(text_translated)

@client.command()
async def animal(ctx, animal: str):
    if (animal := animal.lower()) in ("dog", "cat", "panda", "fox", "bird", "koala"):
        fact_url = f"https://some-random-api.ml/facts/{animal}"
        image_url = f"https://some-random-api.ml/img/{'birb' if animal == 'bird' else animal}"

        async with request("GET", image_url, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                image_link = data["link"]

            else:
                image_link = None

        async with request("GET", fact_url, headers={}) as response:
            if response.status == 200:
                data = await response.json()

                embed = Embed(title=f"{animal.title()} fact",
                                description=data["fact"],
                                colour=ctx.author.colour)
                if image_link is not None:
                    embed.set_image(url=image_link)
                await ctx.send(embed=embed)

            else:
                await ctx.send(f"API returned a {response.status} status.")

    else:
        await ctx.send("No facts are available for that animal.")






client.run(TOKEN)