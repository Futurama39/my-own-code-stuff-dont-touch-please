import discord
import time
import re

client = discord.Client()

lc = 0

responses = [[]]

async def niceappend(uid,response):
    global lc
    row = [uid,response,0,0]
    responses.append([])
    responses[lc].extend(row)
    lc = lc + 1
    return True

async def responded(uid, i=0):
    global lc
    while(i<lc):
        if uid in responses[i]:
            return True
        else:
            i=i+1
    return False

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == "whome":
        await message.channel.send(message.author.id)

    if message.startswith == "help" or "Help":
        await message.channel.send('No help is coming')
        time.sleep(3)
        await message.channel.send('Run.')
        
    if message.content.startswith("♥res "):
<<<<<<< HEAD
        if responded(message.author.id):
            await message.channel.send("You already responded once!")
=======
        p_response = re.sub('♥res ','',message.content)
        if niceappend(message.author.id,p_response):
            await message.channel.send("Got it")
            await message.channel.send("Words: " + len(s.split(message.author.id)))
>>>>>>> abf49608e36b813f89c5189a023f00d12c7312b8
        else:
            p_response = re.sub('♥res ','',message.content)
            if niceappend(message.author.id,p_response):
                await message.channel.send("Got it")
            else:
                await message.channel.send("Error lol")

    if message.content == "showme":
        await message.channel.send(responses)


with open('token.txt','r') as Token:
    token = Token.read().replace('\n','')

client.run(token)
