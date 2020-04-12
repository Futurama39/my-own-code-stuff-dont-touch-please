import json
import re

def fucking_americans_please_use_a_standardised_system_for_your_date_formats_i_want_to_die_now(item):
    stupid_american_format = re.findall(r'[0-9]{1,2}',item)
    day = stupid_american_format[1]
    month = stupid_american_format[0]
    year = stupid_american_format[2]

    if len(day) == 1:
        day = '0'+day
    if len(month) == 1:
        month = '0'+month
    if len(year) == 2:
        year = '20'+year

    iso_date = year+'-'+month+'-'+day
    return iso_date

with open('D:\\Spews of creativity\\pyshit\\my-own-code-stuff-dont-touch-please\\Python\\csvjson.json','r') as infile:
    table = json.load(infile)

dateslist = list(table[0].keys())
dateslist = dateslist[4::]

outtable = []

for col in table:
    for item in dateslist:
        if col[item] != 0:
            date = item
            break
    if item != '':
        entry = []
        entry.append(col['Province/State'])        
        entry.append(col['Country/Region'])
        entry.append(fucking_americans_please_use_a_standardised_system_for_your_date_formats_i_want_to_die_now(item))
        outtable.append(entry)

print(outtable)
with open('out.json','w') as outfile:
    outfile.write(json.dumps(outtable))
