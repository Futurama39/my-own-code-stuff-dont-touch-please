import json
import random
import re
import time

import discord  # pip install -U git+https://github.com/Rapptz/discord.py@rewrite#egg=discord.py[voice]

client = discord.Client()
prefix = "\\"


class SavingError(Exception):
    pass

class DumpingError(Exception):
    pass

class WrongVotingState(Exception):
    pass

class ResponsesOverflow(Exception):
    pass    

with open('main.txt','rb') as a:
    try:
        Bot = json.loads(a.read())
        responses = Bot[0]
        admins = Bot[1]
        lc = Bot[2]
        voting = Bot[3]
        sessions = Bot[4]
        print("Main file loaded!")
    except json.decoder.JSONDecodeError:
        responses = []
        admins = ['195606469792497696']
        lc = 0
        voting = False
        sessions = []
        Bot = [responses,admins,lc,voting,sessions]
        print("No recognised main file, creating header")
    except FileNotFoundError:
        raise Exception('Create main.txt, dummy!')

def is_admin(uid):
    if str(uid) in admins:
        return True

def dump():
    try:
        open('main.txt','w').close()
        return True
    except:
        return False

def save(i=0):
        with open('main.txt','w') as a:
            a.write(json.dumps(Bot))
        return True

def save_response(uid,response):
    response_p = re.sub(r'\\respond ','',response)
    row = [uid,response_p,[],[]]
    responses.append(row)
    return True

def responded(uid, i=0):
    global lc
    while(i<lc):
        if uid in responses[i]:
            return True
        else:
            i=i+1
    return False

def err_dump():
    global responses, admins, lc ,voting ,Bot
    print("Responses = "+ str(responses))
    print("Admins = "+ str(admins))
    print("lc = "+str(lc))
    print("voting = "+str(voting))
    print("Bot = "+str(Bot))

def gen_responses(uid):
    print(responses)
    s_responses = responses.copy()
    random.shuffle(s_responses)
    print(s_responses)
    print(s_responses[1][2])
    print(s_responses[1][3])
    def pick_responses(uid,i=0,j=0):
        try:
            while j < 2:
                if s_responses[i][2] or s_responses[i][3] == uid:
                    i=i+1
                elif j == 0:
                    pick1 = s_responses[i]
                    i=i+1
                    j=j+1
                else:
                    pick2 = s_responses[i]
                    return [pick1,pick2]
        except:
            raise ResponsesOverflow()
    
    def list_appropriate(picks):
        return [[picks[0][0],picks[0][1]],[picks[1][0],picks[1][1]]]

    return list_appropriate(pick_responses(uid))
    
def create_sess(uid):
    if uid in sessions:
        dump_sess(uid)
    sessions.append([uid,gen_responses(uid)])

def dump_sess(uid):
    del sessions[sessions.index(uid)]
    
    

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    try:
        global responses,voting
        send = message.channel.send
        ath = message.author
        uid = message.author.id
        start = message.content.startswith
        msg = message.content

        if ath == client.user:
            return

        def command(keywd,a_only=False,v_only=False,s_only=False):
            global prefix, voting
            if msg == prefix+keywd or start(prefix+keywd):
                if a_only == True and not is_admin(uid):
                    raise PermissionError
                elif v_only and not voting:
                    raise WrongVotingState
                elif s_only and voting:
                    raise WrongVotingState
                else:
                    return True

        if command("isvoting"):
            await send(voting)

        if command("do_voting",True,False,True):
            voting = True
            save()
            await send("Voting has begun")

    
        if command("amadmin"):
            await send(is_admin(uid))

        if command("makeadmin",True):
                admin = re.sub("makeadmin ",'',msg)
                admins.append(admin)
                print(str(uid)+ " made " + str(admin) + " admin")
                await send("Made <@" + str(uid)+"> Admin!")

        if command("pingme"):
            await send("<@"+ str(uid)+">")
        
        if command("vote",False,True):
            create_sess(uid)
            print("testing")
        
        if command("respond",False,False,True):
            if not responded(uid) or is_admin(uid):
                if save_response(uid,msg):
                    try:
                        save()
                    except:
                        raise SavingError
                    await send("Got it")
                    await send("Words: " + str(len(str.split(msg))-1))
            else:
                await send("You already responded once!")
            return

        if command("showme",True):
            await send(responses)
    
        if command("save",True):
            try:
                save()
                await send("Saved")
            except:
                raise SavingError()

        if command("dump",True):
                try:
                    dump()
                    global lc
                    lc = 0
                    responses = []
                    await send("Dumped!")
                    print("Responses dumped by: " + str(uid))
                except:
                    raise DumpingError()

    except PermissionError:
        print(str(uid)+ "tried to acces an admin command")
        await send("Not enough permissions!")

    except WrongVotingState:
        if voting:
            await send("Command not processed\nOnly avalible when there's no voting!")
        else:
            await send("Command not processed\nOnly avalible when voting is enabled")    

    except ResponsesOverflow:
        await send("You already voted!")

    except SavingError:
        print("Saving Error!\n\n")
        err_dump()
        await send("Saving Error!")

    except DumpingError:
        print("Dumping error!\n\n")
        err_dump()
        await send("Dumping Error!")

    '''except:
        print("Unknown error!\n\n")
        err_dump()
        await send("Unknown error!")'''






with open('token.txt','r') as Token:
    token = Token.read().replace('\n','')

client.run(token)
