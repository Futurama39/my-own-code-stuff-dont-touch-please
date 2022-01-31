# Discord DM message tool

Reads discord text channel logs and makes data tables from them  
presumably all versions are a bit broken so just clone from master and hope

## Dependencies
All depend on [Discord Chat Exporter](https://github.com/Tyrrrz/DiscordChatExporter) and getting the logs from there.
Install and  run the program, for your user token [they have a guide](https://github.com/Tyrrrz/DiscordChatExporter/wiki/Obtaining-Token-and-Channel-IDs)

Python specific dependencies:
 ```pandas, python-dateutil, plotly```

And then a bunch of imports that should be in the base python libs

## Getting the logs
For safety before download click on the cog and for time format setting input ```u```
In discord chat exporter, navigate the GUI to download the channels you whish.
When prompted for a format, select JSON and then save to a folder without any .json files. You will be asked to provide a path to this folder later.

## Running 
If you want a graph you'll want to run graph.py
If you want to get the pandas dataframe import table.py and run main which returns a dataframe

## Config
If a config file is not present, the program will prompt user for parameters which are then saved
WARNING : right now there's no support for multiple config files. If at least one file is found the first one will be used
## old_dscgraphs
This section is for the old_dscgraphs folders, they have more launch options and such but they will not be developed, if you're interested you'll be launching dscgraphs.py and following the old readme below
### Getting the text logs

This project depends on the [Discord Chat Exporter](https://github.com/Tyrrrz/DiscordChatExporter)
Install and  run the program, for your user token [they have a guide](https://github.com/Tyrrrz/DiscordChatExporter/wiki/Obtaining-Token-and-Channel-IDs)
**Important**: Click on the cog in the upper right and select the time format to be ```s```. Then export desired DMs in TXT form into a folder. Prefferably one where those text files will be the only text files there

### Dependencies
These files depend on ```matplotlib``` and ```numpy```
### Using the python scripts

If you want to just create the tables all dependencies should be part of the standard python libs  
dscgraphs.py depends on matplotlib and numpy (doesn't work at the moment)

Once the text logs are in a folder, open dscmsg.py and interact with the CLI

### Config files

If you want to make a table, dscmsg requires you create a config file for your settings before continuing
they are essentially JSON files

If the program gives you a warning about old config files, you can either delete them and make new ones, or open the file in a text editor and append an entry into the JSON list that looks same as *path*

## Shoutouts

Lily for helping me with the datetime module  
Yarin for keeping my sanity and helping with like everything
