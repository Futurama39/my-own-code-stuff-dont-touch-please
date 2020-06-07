'''This will make data tables for your DMs or other server channels, getting the total messages per day, month, or just the messages in a month, or word counting!
    I use the TXT output of https://github.com/Tyrrrz/DiscordChatExporter a really nice program that's easy to use
    
    IMPORTANT: ON THE APP, SET THE DATE FORMAT TO "s" (the ISO standard format)

    forward angry letters to Futurama39#3939

    advice : you should have as much system memory free as is the file size of the biggest DM you have
    '''


#edit these vars for the desired outcome

time_mode = 2 #[0=years,1=months,2=days]
words = False #messages/words
past = True #wheter to output #of messages IN the time period or SINCE the time period (so the latter being a cumulative count)
path = 'C:\\Users\\Uzivatel\\Documents\\di_exports\\new\\' #path to the folder with the text files
username = r'' #match against messages from just one person, leave empty to disable NOTE: parses regexes too if you're into that
#NOTE: use a folder where the extracted files are the only text files in the folder


from glob import glob #all of these should be the part of the standard python libs
import re
import csv
import datetime
import os.path

out = [[]] #list of the outputs
out_control = 0 #iterable to know which row we should out into
message_count = 1
ignore = False #for attachements the txt displays {Attachement} or so, after that until the next timestamp, we can ignore counting words
startslist = []

if ((time_mode not in range(3)) or ((type(words) or type(past)) != bool) or (type(username) != str)):
    print('Inital variables do not have expected values?')

def isoify(obj):
    return str(obj.year)+'-'+str(obj.month)+'-'+str(obj.day)

def wordcount(string):
    if string != [] or string =='\n':
        a = re.sub(r'http.*\.\S+','',string) #we do not want to count words contaitned within links
        a = re.findall(r'[., !?;"¡():{}\n\[\]”\\/\u2000-\u206f`]+|.\Z',a)
        return len(a)
    else:
        return 0

def is_date(line): #looks for the next line with a timestamp and returns that timestamp
        find = re.findall(r'^\[([0-9]{4})-([0-9]{2})-([0-9]{2}).*#[0-9]{4}',lines[line]) #regex to find the timestamp
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

def findusername():
    global username, lines
    result = re.fullmatch(username,lines[line])
    if result == None:
        return False
    else:
        return True

files = glob(path+'*.txt')
print('found ',len(files),' text files!')
#print(files)
for log in files:
    with open(log,'r',1,"UTF8") as l:
        lines = l.readlines() #serialies all lines of txt into list line by line
        lines = lines[:-6:] #get rid of the last six lines
        name = re.sub(r"Channel:.+\/ ","",lines[2]) #name that will show up, either the channel name, or the person you've DM'd
        name = re.sub('\\n',"",name) #gtfo newline
        out.insert(out_control,[name]) #the first item in the row is the name, then the values are put in
        date = is_date(5)[0]
        startslist.append(date)
        if words:
            wordlist = []
            w_control = 0
            for line in range(6,len(lines)):
                if is_date(line) != None:
                    if username =='' or findusername():
                        newdate = is_date(line)[0]
                        ignore = False
                        if newdate[time_mode] == date[time_mode]: #dates are same, message has been sent on the same date
                            pass
                        else:   #the dates are different
                            try:
                                new = newdate
                                newdate = datetime.date(int(newdate[0]),int(newdate[1]),int(newdate[2]))
                                date = datetime.date(int(date[0]),int(date[1]),int(date[2])) # i need to load these two into the datetime class because it will do the date diff for me
                                diff = timediff(time_mode,newdate,date)
                                for i in range(diff-1):
                                    wordlist.append('')
                                    w_control+=1
                                date = new
                                w_control+=1
                            except ValueError:
                                pass
                    else:
                        ignore = True
                else:
                    if lines[line] == '{Attachments}\n' or lines[line] == '{Embed}\n': #sent attachements or things shown in file embeds, we want to shed this
                        ignore = True #embeds or attachements always at the end of message, we can just ignore all text until new message
                    if not(lines[line] == '\n' or ignore):  #words to be counted, I just get all the words into a seperate list, delimited properly by days/mon/yrs and then count them at the end
                        while len(wordlist) <= w_control:
                            wordlist.append('')
                        wordlist[w_control] += lines[line]
            if not past:
                for i in wordlist:
                    out[out_control].append(wordcount(i))
            else:
                a=0
                for i in wordlist:
                    a+= wordcount(i)
                    out[out_control].append(a)                    

        else:   #counts messages
            num = 1 #since we start the for loop after the very first message, it has to be counted here
            for line in range(6,len(lines)):
                newdate = is_date(line)
                if newdate != None:
                    if username =='' or findusername(): #TODO: ugly, make the username func parse regexes too
                        newdate = newdate[0]
                        if newdate[time_mode] == date[time_mode]: #dates are same, message has been sent on the same date
                            num+=1   
                        else:
                            try:   #the dates are different
                                new = newdate
                                newdate = datetime.date(int(newdate[0]),int(newdate[1]),int(newdate[2]))
                                date = datetime.date(int(date[0]),int(date[1]),int(date[2])) # i need to load these two into the datetime class because it will do the date diff for me
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
                                else:
                                    num+=1
                            except ValueError:      #some messages may appear like the timestamps and get recognized as such
                                pass
            out[out_control].append(num)
    print(files[out_control],' converted')
    out_control+=1 #opening a new file so we want to start a new row
out = out[:-1:]
con = 0

if startslist == []:
    print('No files ran, is the path correct?')

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

for i in range(len(startslist)):    #extending all rows so they are pinned to the same starting date
    for j in range(deltalist[i]):
        out[i].insert(1,0)

end = len(out[0])                   #need to find the largest list for establishing the same end date
for i in range(len(out)):
    if len(out[i])>end:
        end = len(out[i])
if past:
    for i in range(len(out)):           #we extend the ends of the lists so they are same size
        while len(out[i])<end:          #we can assume that since the dm didn't have any more recent entries that no new messages happened
            out[i].append(out[i][-1])   #in the case of past == True we just append the last value from the list to it
else:
    for i in range(len(out)):           #in the case of past == False we just need to add 0 instead of the last value
        while len(out[i])<end:          
            out[i].append(0)    
axis = ['']                             #constructing the time axis

j = minimum
if time_mode==0:                        #the time axis is constructed in the ISO date format
    axis.append(isoify(j))
    for i in range(end):
        j = datetime.date(j.year+1,j.month,j.day)
        axis.append(isoify(j))
elif time_mode==1:
    axis.append(isoify(j))
    for i in range(end):
        j = datetime.date(j.year + ((j.month + 1) // 13), (j.month % 12) + 1, j.day)
        axis.append(isoify(j))
else:
    for i in range(end):
        axis.append(isoify(minimum+datetime.timedelta(days=i)))
out.insert(0,axis)

fileiter = 0
while True:
    if os.path.isfile(path+'out'+str(fileiter)+'.csv'):
        fileiter+=1
    else:
        break

with open (path+'out'+str(fileiter)+'.csv','w+',1,'UTF-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(out)

print("done")