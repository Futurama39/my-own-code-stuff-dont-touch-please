'''
When imported the chart_get function returns a data table

When ran individually the result is exported into a csv file

This will make data tables for your DMs or other server channels, getting the total messages per day, month, or just the messages in a month, or word counting!
I use the TXT output of https://github.com/Tyrrrz/DiscordChatExporter a really nice program that's easy to use

Help for that program availible on their github
    
IMPORTANT: ON THE APP, SET THE DATE FORMAT TO "s" (the ISO standard format)

forward angry letters to Fewtoo#3939

NOTE: would a time mode for hours work? probably. would any sheet software freak out on seeing a 20 by 24k table? also probably
google sheets already breaks with my normal time mode so...
'''

from glob import glob #all of these should be the part of the standard python libs
import re
import csv
import datetime
import os
import hashlib #possible missing of the MD5 module if FIPS compliant python download
import json

out = [[]] #list of the outputs
'''
list is structured thusly:
[
    [date (in ISO format),date,...]
    [username,int,int,...]
    ...

]
'''

out_control = 0 #iterable to know which row we should out into
startslist = []

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


#print(files)
def chart_get():
    #
    # kidnda choppy since main loop was not originally assigned as a fuction 
# kidnda choppy since main loop was not originally assigned as a fuction 
    # kidnda choppy since main loop was not originally assigned as a fuction 
    # but that had to change because normal sheets software kept breaking so i now needed to backwork imporing it into another program
    #
    global out, lines, line, out_control, ignore, startslist,path,words,past,username
    ignore = False #for attachements the txt displays {Attachement} or so, after that until the next timestamp, we can ignore counting words
    files = glob(path+os.sep+'*.txt')
    print('found ',len(files),' text files!')

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
    elif time_mode==1:                      #different reconstruction for the months axis
        axis.append(isoify(j))
        for i in range(end):
            j = datetime.date(j.year + ((j.month + 1) // 13), (j.month % 12) + 1, j.day)
            axis.append(isoify(j))
    else:
        for i in range(end):
            axis.append(isoify(minimum+datetime.timedelta(days=i)))
    out.insert(0,axis)
    if __name__ == "__main__": #only out to csv if ran individually
        with open (outpath+os.sep+'out-'+outname+'.csv','w+',1,'UTF-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(out)

        print("done")
    else:
        return out
def create_settings_file(filename=""):
    global setting
    #NOTE:settings are validated here so i just hope that i don't need to check them on load
    print("Choose a time mode:\n0 = Measure by years\n1 = Measure by months\n2 = Measure by days\n")
    while True:                                                     #input validation because yay i have to
        time_mode = input()                                         #i basically go thru this process for every option
        try:
            time_mode = int(time_mode)
            if 0 >= time_mode >= 2:
               raise TypeError 
            break
        except TypeError:
            print("Please enter a number from 0 to 2!")
            continue
    setting = [time_mode]
    print("Should the count be my number of messages or by word count?\n0 = Count by messages\n1 = Count by word count")
    while True:                                                     #input validation because yay i have to
        words = input()                                         #i basically go thru this process for every option
        try:
            words = int(words)
            if 0 >= words >= 1 :
               raise TypeError
            elif words == 0:
                words = False
            elif words == 1:
                words = True
            else:
                raise Exception 
            break
        except TypeError:
            print("Please enter a number from 0 to 1!")
            continue
    setting.append(words)
    print("Should the table count the messages since the date or on the date\n0 = Excplicit value on that date\n1 = Cumulative value since that day")
    while True:                                                     #input validation because yay i have to
        past = input()                                         #i basically go thru this process for every option
        try:
            past = int(past)
            if 0 >= past >= 1 :
               raise TypeError
            elif past == 0:
                past = False
            elif past == 1:
                past = True
            else:
                raise Exception 
            break
        except TypeError:
            print("Please enter a number from 0 to 1!")
            continue
    setting.append(past)
    print("What is the path to the folder with the text files?\nFull path:")
    while True:
        path = input()
        if os.path.isdir(path):
            break
        else:
            print("The entered file path does not point to a folder!")
    setting.append(path)
    print("Filetring usernames\nIf you want to look for messages from one user type the name here\nRegular expressions are allowed\nso you can enter just a part of the username but full name with discrim (like \"me#0001\") reccomended\n\nIf you do not whish to filter for users leave empty\n")
    username = input()
    setting.append(username)
    if filename == "":
        print("\nEnter a file name for the settings file:")
        filename = input()+".dscjson"
    print("Where do you want the csv file to be outputted? (file path)\nOptional, if left empty the location of the text files will be selected")
    while True:
        outpath = input()
        if os.path.isdir(outpath):
            break
        elif outpath == "":
            outpath = path
        else:
            print("The entered file path does not point to a folder!")
    setting.append(outpath)
    with open(filename,"w+") as f:
        json.dump(setting,f)
    return 1

def choosefile():
    global time_mode, words, past, path, username, outpath
    while True: #keep trying to load a file until succesful
        '''try:    #even if something shits itself we need to FIND THE FILE'''
        settinglist = glob("*.dscjson")
        if len(settinglist) == 0:   #no files found
            print("No setting file found...\nCreating new one")
            create_settings_file()
        else: #we have at least one file
            print("Setting file(s) detected!\nChoose desired file:")
            for i in range(len(settinglist)):                               #for loop every file in glob list and print it out for the user
                print("["+str(i)+"] - "+settinglist[i])
            i+=1
            print("["+str(i)+"] - Create a new settings file\n\n")           #last option always create new
            chosenfile = int(input()) #user chooses a file
            if chosenfile == len(settinglist):
                print("No setting file found...\nCreating new one")
                create_settings_file()
            else:
                with open(os.getcwd()+os.sep+settinglist[chosenfile],"r") as f:
                    setting = json.load(f)
                time_mode = setting[0] #[0=years,1=months,2=days]
                words = setting[1] #messages/words
                past = setting[2] #wheter to output #of messages IN the time period or SINCE the time period (so the latter being a cumulative count)
                path = setting[3] #path to the folder with the text files
                username = setting[4] #match against messages from just one person, leave empty to disable NOTE: parses regexes too if you're into that
                try:
                    outpath = setting[5] #path to out the file
                except EOFError:
                    print("\n\nWARNING: OUTPATH WAS NOT SPECIFIED\nTHE FILES PATH WILL BE USED\nTHIS INDICATES SETTINGS FILES CREATED WITH AN OLD VERSION OF THE PROGRAM\nplease upgrade uwu <3\n\n")
                    outpath = path #legacy backsupport
                return 1
        '''except Exception as f:
            raise f'''


if __name__ == "__main__":
    choosefile()
    hashsetting = json.dumps(setting) #creates hash, better to move into a function?
    outname = hashlib.md5()
    outname.update(hashsetting.encode('utf-8'))
    outname = outname.hexdigest()
    chart_get()
    print("Press any key to exit.")
    a = input()