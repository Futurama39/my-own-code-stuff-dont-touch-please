import json
import random
import re
import time

import discord  # pip install -U git+https://github.com/Rapptz/discord.py@rewrite#egg=discord.py[voice]

client = discord.Client()
prefix = "\\"


class SavingError(Exception):   #For when saving the responses + votes to a file fails
    pass

class DumpingError(Exception):  #For when erasing the current responses + votes fails
    pass

class WrongVotingState(Exception):  #For if a command for voting is accesed in the submission phase and vice versa
    pass

class ResponsesOverflow(Exception):     #Voting fuction didn't pick any responses
    pass    

with open('main.txt','rb') as a:    #Open the responses file and extract the list from them
    try:
        Bot = json.loads(a.read())
        responses = Bot[0]
        admins = Bot[1]
        lc = Bot[2]
        voting = Bot[3]
        sessions = Bot[4]
        print("Main file loaded!")
    except json.decoder.JSONDecodeError:    #file empty/unusable, creates an empty header
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

def save_response(uid,response):    #from raw message into list entry
    response_p = re.sub(r'\\respond','',response)
    row = [uid,response_p,[],[]]
    responses.append(row)
    return True

def responded(uid, i=0):    #checks if user has responded
    global lc
    while(i<lc):
        if uid in responses[i]:
            return True
        else:
            i=i+1
    return False

def err_dump():             #for when an error occurs, dump the state of everything
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
    def pick_responses(uid,i=0,j=0):    #pick two random respnses the person hadn't voted on
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
    
    def list_appropriate(picks):    #serialize the two picks into a 2x2 matrice
        return [[picks[0][0],picks[0][1]],[picks[1][0],picks[1][1]]]

    return list_appropriate(pick_responses(uid))
    
def create_sess(uid): #get rid of this
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

    try:        #this is the core of the whole program
        global responses,voting         #couple of shorthands for more readable code
        send = message.channel.send     #send a message
        ath = message.author            #message author (used once)
        uid = message.author.id         #Id of message author
        start = message.content.startswith  #Function! if the message stars with var, returns True
        msg = message.content           #The sent message

        if ath == client.user:          #so the bot doesn't respond to himself 
            return

        def command(keywd,a_only=False,v_only=False,s_only=False):  #A wrapper that takes a keyword and checks against voting states and admin permissions
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
            await send(voting) #(that's a boolean)

        if command("do_voting",True,False,True): #end responding and begin voting
            voting = True
            save()
            await send("Voting has begun")

    
        if command("amadmin"):  #asks if user who sent the message is an administator
            await send(is_admin(uid))

        if command("makeadmin",True): #make a person admin, also dumps who made who admin
                admin = re.sub("makeadmin ",'',msg)
                admins.append(admin)
                print(str(uid)+ " made " + str(admin) + " admin")
                await send("Made <@" + str(uid)+"> Admin!")

        if command("pingme"):
            await send("<@"+ str(uid)+">")
        
        if command("vote",False,True):
<<<<<<< HEAD
            create_sess(uid)            
            print("testing")
=======
            create_sess(uid)    #gonna remove this soon, hopefully
            print("testing")    #(does effectively nothing)
>>>>>>> d36427f6f1d52e08e8d398972f53604ca37fa460
        
        if command("respond",False,False,True):
            if not responded(uid) or is_admin(uid):    #allows admins to respond multiple times, for testing
                if save_response(uid,msg):
                    try:
                        save() #important, save after every response
                    except:
                        raise SavingError
                    await send("Got it")
                    await send("Words: " + str(len(str.split(msg))-1))
            else:
                await send("You already responded once!")
            return

        if command("showme",True): #sends responses in the chat
            await send(responses)
    
        if command("save",True):  #manual save
            try:
                save()
                await send("Saved")
            except:
                raise SavingError()

        if command("dump",True):       #dispose of the responses list
                try:
                    dump()
                    global lc
                    lc = 0
                    responses = []
                    await send("Dumped!")
                    print("Responses dumped by: " + str(uid))
                except:
                    raise DumpingError()

    #NOW ENTERING : EXCEPTION HANDLING PART

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

    #acutally use this in nomral releases, just commented out for more responsive debugging 
    '''except:
        print("Unknown error!\n\n")
        err_dump()
        await send("Unknown error!")'''






with open('token.txt','r') as Token:
    token = Token.read().replace('\n','')

client.run(token)
