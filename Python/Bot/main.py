import discord
import time
import re
import json

client = discord.Client()

admins = ['195606469792497696']
lc = 0

def is_admin(uid):
    if str(uid) in admins:
        return True


with open('responses.txt','rb') as a:
    try:
        responses = json.loads(a.read())
        print("Responses file loaded!")
    except json.decoder.JSONDecodeError:
        responses =[[]]
        print("No recognised responses file, creating header")

def dump():
    try:
        open('responses.txt','w').close()
        return True
    except:
        return False

def save(i=0):
    with open('responses.txt','w') as a:
        a.write(json.dumps(responses))
    return True

def respond(uid,response):
    response_p = re.sub('♥res ','',response)
    global lc
    row = [uid,response_p,0,0]
    responses.append([])
    responses[lc].extend(row)
    lc = lc + 1
    return True

def responded(uid, i=0):
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

    global responses
    send = message.channel.send
    ath = message.author
    uid = message.author.id
    start = message.content.startswith
    msg = message.content

    if ath == client.user:
        return
    
    if msg == "amadmin":
        if is_admin(uid):
            await send("Yes")
        else:
            await send("No")
        return

    if start("makeadmin") and is_admin(uid):
        admin = re.sub("makeadmin ",'',msg)
        admins.append(admin)
        print(str(uid)+ " made " + str(admin) + " admin")
        await send("Made <@" + str(uid)+"> Admin!")


    if msg == "whome":
        await send(uid)
        return

    if msg == "pingme":
        await send("<@"+ str(uid)+">")
        return
        
    if start("♥res "):
        if not responded(uid) or is_admin(uid):
            if respond(uid,msg):
                await send("Got it")
                save()
                await send("Words: " + str(len(str.split(msg))-1))
        else:
            await send("You already responded once!")
        return

    if msg == "showme" and is_admin(uid):
        await send(responses)
        return
    
    if msg == "save" and is_admin(uid):
        if save():
            await send("Saved")
        else:
            await send("Failed to save")
        return

    if msg == "dump" and is_admin:
        if dump():
            global lc
            lc = 0
            responses = [[]]
            await send("Dumped!")
            print("Responses dumped by: " + str(uid))
        else:
            await send("Something went wrong!")
        return





with open('token.txt','r') as Token:
    token = Token.read().replace('\n','')

client.run(token)
