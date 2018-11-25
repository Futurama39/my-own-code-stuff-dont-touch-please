import discord
import time
import re
import json

client = discord.Client()

admins = ['195606469792497696']
lc = 0

class SavingError(Exception):
    pass

class DumpingError(Exception):
    pass


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

    try:
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

        if start("makeadmin"):
            if is_admin(uid):
                admin = re.sub("makeadmin ",'',msg)
                admins.append(admin)
                print(str(uid)+ " made " + str(admin) + " admin")
                await send("Made <@" + str(uid)+"> Admin!")
            else:
                raise PermissionError()


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
                    try:
                        save()
                    except:
                        raise SavingError
                    await send("Words: " + str(len(str.split(msg))-1))
            else:
                await send("You already responded once!")
            return

        if msg == "showme":
            if is_admin(uid):
                await send(responses)
            else:
                raise PermissionError()
            return
    
        if msg == "save":
            if is_admin(uid):
                save()
            else:
                raise PermissionError()
            return

        if msg == "dump":
            if is_admin(uid):
                try:
                    dump()
                    global lc
                    lc = 0
                    responses = [[]]
                    await send("Dumped!")
                    print("Responses dumped by: " + str(uid))
                except:
                    raise DumpingError()
            return

    except PermissionError:
        print(str(uid)+ "tried to acces an admin command")
        await send("Not enough permissions!")

    except SavingError:
        print("Saving Error!")
        print("Responses = "+ str(responses)+ "\n user = "+ str(uid) + "\n message = " + str(msg))
        await send("Saving Error")

    except DumpingError:
        print("Dumping error!")
        print(" Responses = "+str(responses)+ "\n lc = " + str(lc)+ "\n message = "+str(msg)+ "\n user = "+str(uid))
        await send("Dumping Error!")

    except:
        print(" Responses = "+str(responses)+ "\n lc = " + str(lc)+ "\n message = "+str(msg)+ "\n user = "+str(uid))
        print("Unknown error!")
        await send("Unknown error!")






with open('token.txt','r') as Token:
    token = Token.read().replace('\n','')

client.run(token)
