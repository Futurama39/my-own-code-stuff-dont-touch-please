'''This will make data tables for your DMs or other server channels, getting the total messages per day, month, or just the messages in a month, or word counting!
    I use the TXT output of https://github.com/Tyrrrz/DiscordChatExporter a really nice program that's easy to use
    
    NOTE: PLACE THIS FILE IN THE SAME FOLDER AS THE TEXT FILE OUTPUTS AND JUST THE OUTPUTS FOR BEST OUTCOMES'''

from glob import glob
import re
import csv

#edit these vars for the desired outcome

time_mode = 0 #[days,months,years]
words = False #messages/words

out = [] #list of the outputs
out_control = -1 #iterable to know which row we should out into
line = 5 # for which line are we currently working with 

def next_message():
    global line
    find = re.match(r'\[([0-9]{2})-([A-Z][a-z]{2})-([0-9]{2}) [0-9]{2}:[0-9]{2} (AM|PM)\].*#[0-9]{4}$',lines[line]) #regex to find the timestamp
    while True:
        if find != '': #if regex empty, its not a new message
            return find
        line+=1
    


files = glob('*.txt')
for log in files:
    out_control+=1 #opening a new file so we want to start a new row
    line = 5 
    with open(log) as l:
        lines = l.readlines #serialies all lines of txt into list line by line
        name = re.sub("Channel: ","",lines[2]) #name that will show up, either the channel name, or the person you've DM'd
        out[out_control]=[name,]
        if words:
            pass #TODO : the word count loop
        else:   #counts messages
            date = next_message()[time_mode]
            while True:
                message_count=1
                while next_message != date:
                    message_count+=1
                out[out_control].append(message_count)

print(out)




