import discord
import time
import re
import yaml

client = discord.Client()

lc = 0
store = open("responses.txt","r+")
responses = yaml.load('responses.txt')
if 'responses' in locals():
    responses = [[]]

def save():
    yaml.dump({responses}, responses.yaml)
    return True

def niceappend(uid,response):
    global lc
    global store
    row = [uid,response,0,0]
    responses.append([])
    responses[lc].extend(row)
    lc = lc + 1
    return True

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == "whome":
        await message.channel.send(message.author.id)

    if message.content == "help":
        await message.channel.send('No help is coming')
        time.sleep(3)
        await message.channel.send('Run.')
        
    if message.content.startswith("♥res "):
        p_response = re.sub('♥res ','',message.content)
        if niceappend(message.author.id,p_response):
            await message.channel.send("Got it")
        else:
            await message.channel.send("Error lol")

    if message.content == "showme":
        await message.channel.send(responses)
    
    if message.content == "save":
        if save():
            await message.channel.send("Saved")


with open('token.txt','r') as Token:
    token = Token.read().replace('\n','')

client.run(token)
