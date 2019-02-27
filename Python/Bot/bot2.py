import discord #pip install -U git+https://github.com/Rapptz/discord.py@rewrite#egg=discord.py[voice]
import re
import random
import math

client = discord.Client()
prefix = "\\"
Mines = []
Grid = []
string = ''
replist = [u'||      1     ||',u'||    2   ||',u'||    3   ||',u'||   4   ||',u'||    5   ||',u'||    6   ||',u'||    7   ||',u'||   8   ||',u'||    9   ||']

    
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))          
        

@client.event
async def on_message(message):

        def makeboard(size,num):
            global Mines, Grid, string
            Mines = []
            Grid = []
            string = ''
            def makegrid(size,i=0):
                while i < size**2:
                    Grid.append(i)
                    i=i+1
            def getmines(num,size,i=0):
                while i < num:
                    Mines.append(random.randint(0,(size**2)-1))
                    i = i+1
            def finalizeboard(size,i=0,j=0):
                for n in Mines:
                    Grid[n] = 'b'
                while i < size**2:
                    if Grid[i] == 'b':
                        pass
                    else:
                        if i % size ==0:
                            check = [i-size,i-size+1,i+1,i+size,i+size+1]
                        elif i % size == size-1:
                            check = [i-size-1,i-size,i-1,i+size-1,i+size]
                        else:
                            check = [i-size-1,i-size,i-size+1,i-1,i+1,i+size-1,i+size,i+size+1]
                        for n in check:
                            if n < 0 or n >= size**2:
                                pass
                            else:
                                if Grid[n] == 'b':
                                    j=j+1
                        Grid[i] = j
                        j=0
                    i=i+1
            def formatgrid(i=0):
                try:
                    while True:
                        if Grid[i] == 'b':
                            Grid[i] = '||:bomb:||'
                        else:
                            Grid[i] = '||  '+str(Grid[i])+'  ||'
                        
                        i=i+1
                except IndexError:
                    pass
            def makestring(size,i=0):
                global string       #
                while i < (size**2):      
                    string = string + str(Grid[i])  
                    if i % size == size-1 and i !=0:
                        string = string + '\n'
                    i=i+1
                

            makegrid(size)
            getmines(num,size)
            finalizeboard(size)
            formatgrid()
            makestring(size)
            return string   
    

        send = message.channel.send
        ath = message.author
        uid = message.author.id
        start = message.content.startswith
        msg = message.content

        if ath == client.user:
            return

        def command(keywd,a_only=False):
            global prefix
            if msg == prefix+keywd or start(prefix+keywd):
                return True
            else:
                return False
        
        if command("mines"):
            i=0
            size = int(re.sub(r'\\mines ','',msg))
            mines = int(size**(10/9))
            string = makeboard(size,mines)
            sarray = string.split('\n')
            while i < size:
                try:
                    await send(sarray[i])
                    i=i+1
                except:
                    pass
            await send('There are : '+str(len(Mines))+' mines.')
            
            
        
        if command("pingme"):
            await send("<@"+ str(uid)+">")
        if command("wtest"):
            stri = ''
            i=j=0
            while j <8:
                print(stri)
                while i <5 :
                    stri = stri+str(replist[j])
                    i=i+1
                stri = stri+'\n'
                j=j+1
                i=0
            stri= stri+'\n||:bomb:||||:bomb:||||:bomb:||||:bomb:||||:bomb:||'
            await send(stri)
        

  


with open('token.txt','r') as Token:
    token = Token.read().replace('\n','')

client.run(token)
