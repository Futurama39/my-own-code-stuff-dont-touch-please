import discord
import time

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == "help":
        await message.channel.send('No help is coming')
        time.sleep(3)
        await message.channel.send('Run.')

with open('token.txt','r') as Token:
    token = Token.read().replace('\n','')

client.run(token)
