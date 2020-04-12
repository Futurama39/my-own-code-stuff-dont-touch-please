'''This will make data tables for your DMs or other server channels, getting the total messages per day, month, or just the messages in a month, or word counting!
    I use the TXT output of https://github.com/Tyrrrz/DiscordChatExporter a really nice program that's easy to use
    
    IMPORTANT: ON THE APP, SET THE DATE FORMAT TO "s" (the ISO standard format)

    forward angry letters to Futurama39#3939

    advice : you should have as much system memory free as is the file size of the biggest DM you have
    '''


#edit these vars for the desired outcome

time_mode = 1 #[years,months,days]
words = True #messages/words
past = True #wheter to output #of messages IN the time period or SINCE the time period (so the latter being a cumulative count)
path = 'C:\\Users\\Uzivatel\\Documents\\di_exports\\' #path to the folder with the text files
#NOTE: use a folder where the extracted files are the only text files in the folder


from glob import glob #all of these should be the part of the standard python libs
import re
import csv
import datetime

out = [[]] #list of the outputs
out_control = 0 #iterable to know which row we should out into
message_count = 1
num = 1
ignore = False #for attachements the txt displays {Attachement} or so, after that until the next timestamp, we can ignore counting words
startslist = []



def wordcount(string):
    if string != []:
        a = re.sub(r'http.*\.\S+','',string)
        a = re.findall(r'[., !?;"—¡():{}\[\]”\n]+',a)
        num = len(a)
        if re.match(r'[., !?;"—¡():{}\[\]”\n]$',string) != None:
            num -=1
        return num
    else:
        return 0

def is_date(line): #looks for the next line with a timestamp and returns that timestamp
        find = re.findall(r'\[([0-9]{4})-([0-9]{2})-([0-9]{2}).*#[0-9]{4}$',lines[line]) #regex to find the timestamp
        if find != []: #if regex empty, its not a new message
            return find

def timediff(mode,d1,d2):
    a = d1-d2
    if hasattr(a,'days'):
        if time_mode == 0:
            return d1.year - d2.year
        elif time_mode == 1:
            if d1.year != d2.year:
                return (d1.year-d2.year)*12 + (d1.month-d2.month)
            return d1.month - d2.month
        else:
            return a.days
    else:
        return 0

files = glob(path+'*.txt')
for i in range(len(files)):
    out.append('')
print(files)
for log in files:
    line = 6 
    with open(log,'r',1,"UTF8") as l:
        lines = l.readlines() #serialies all lines of txt into list line by line
        lines = lines[:-6:] #get rid of the last six lines
        name = re.sub("Channel: ","",lines[2]) #name that will show up, either the channel name, or the person you've DM'd
        name = re.sub('\\n',"",name) #gtfo newline
        out[out_control]=[name,''] #the first item in the row is the name, then the values are put in
        date = is_date(5)[0]
        startslist.append(date)
        if words:
            try:
                wordlist = []
                w_control = 0
                while True:
                    if is_date(line) != None:
                        newdate = is_date(line)[0]
                        ignore = False
                        if newdate[time_mode] == date[time_mode]: #dates are same, message has been sent on the same date
                            pass
                        else:   #the dates are different
                            new = newdate
                            date = datetime.date(int(date[0]),int(date[1]),int(date[2])) # i need to load these two into the datetime class because it will do the date diff for me
                            newdate = datetime.date(int(newdate[0]),int(newdate[1]),int(newdate[2]))
                            diff = timediff(time_mode,newdate,date)
                            for i in range(diff-1):
                                wordlist.append('')
                                w_control+=1
                            date = new
                            w_control+=1
                        
                    else:
                        if lines[line] == '{Attachments}\n' or lines[line] == '{Embed}\n': #sent attachements or things shown in file embeds, we want to shed this
                            ignore = True #embeds or attachements always at the end of message, we can just ignore all text until new message
                        if not(lines[line] == '\n' or ignore):
                            while len(wordlist) <= w_control:
                                wordlist.append('')
                            wordlist[w_control] += lines[line]
                    line += 1
            except IndexError:
                if not past:
                    for i in wordlist:
                        out[out_control].append(wordcount(i))
                else:
                    a=0
                    for i in wordlist:
                        a+= wordcount(i)
                        out[out_control].append(a)                    

        else:   #counts messages
            try:
                while True:
                    
                    newdate = is_date(line)
                    print(newdate)
                    if newdate != None:
                        
                        newdate = newdate[0]
                        if newdate[time_mode] == date[time_mode]: #dates are same, message has been sent on the same date
                            pass
                        else:   #the dates are different
                            new = newdate
                            date = datetime.date(int(date[0]),int(date[1]),int(date[2])) # i need to load these two into the datetime class because it will do the date diff for me
                            newdate = datetime.date(int(newdate[0]),int(newdate[1]),int(newdate[2]))
                            out[out_control].append(num)
                            diff = timediff(time_mode,newdate,date)
                            for i in range(diff-1):
                                if not past:
                                    out[out_control].append('0')
                                else:
                                    out[out_control].append(num)
                            date = new
                            if not past:
                                num = 1
                        num+=1
                    line+=1
                
            except IndexError:
                out[out_control].append(num)
    print(files[out_control],' converted')
    out_control+=1 #opening a new file so we want to start a new row
con = 0
for i in startslist:    #gets the starting dates and turns then into the datetime format
    startslist[con] = datetime.date(int(i[0]),int(i[1]),int(i[2]))
    con+=1    

minimum = startslist[0]
for i in range(len(startslist)): # i need to lowest date of all of the DMs to synchronise their dates
    if startslist[i] < minimum:
        minimum = startslist[i]

deltalist = []
for i in range(len(startslist)):    #get a list of how much i need to adjust all rows
    deltalist.append(timediff(time_mode,startslist[i],minimum))

for i in range(len(startslist)):
    for j in range(deltalist[i]):
        out[i].insert(2,0)


with open (path+'out.csv','w+') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(out)
print("done")

