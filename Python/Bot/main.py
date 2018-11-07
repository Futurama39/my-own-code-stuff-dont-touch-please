import discord
import time
import re
import json

client = discord.Client()

admins = ['195606469792497696']
lc = 0

async def is_admin(ctx):
    if ctx in admins:
        return True


with open('responses.txt','rb') as a:
    try:
        responses = json.loads(a.read())
        print("Responses file loaded!")
    except json.decoder.JSONDecodeError:
        responses =[[]]
        print("No recognised responses file, creating header")

async def dump():
    with open('responses.txt','w') as a:
        a.write(json.dumps(''))
    return True

async def save(i=0):
    with open('responses.txt','w') as a:
        a.write(json.dumps(responses))
    return True

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
        
    if message.content.startswith("♥res "):
        if responded(message.author.id) and not is_admin(message.author.id):
            await message.channel.send("You already responded once!")
        else:
            p_response = re.sub('♥res ','',message.content)
            if niceappend(message.author.id,p_response):
                await message.channel.send("Got it")
                save()
                await message.channel.send("Words: " + str(len(str.split(message.content))))

    if message.content == "showme" and is_admin(message.author.id):
        await message.channel.send(responses)
    
    if message.content == "save" and is_admin(message.author.id):
        if save():
            await message.channel.send("Saved")

    if message.content == "dump" and is_admin:
        if dump:
            print("Dumped!")
        else:
            print("Something went wrong!")





with open('token.txt','r') as Token:
    token = Token.read().replace('\n','')

client.run(token)
