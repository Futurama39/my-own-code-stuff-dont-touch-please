# Discord DM message tool

Reads discord text channel logs and makes data tables from them
presumably all versions are a bit broken so just clone from master and hope 

## Getting the text logs

This project depends on the [Discord Chat Exporter](https://github.com/Tyrrrz/DiscordChatExporter)
Install and  run the program, for your user token [they have a guide](https://github.com/Tyrrrz/DiscordChatExporter/wiki/Obtaining-Token-and-Channel-IDs)
**Important**: Click on the cog in the upper right and select the time format to be ```s```. Then export desired DMs in TXT form into a folder. Prefferably one where those text files will be the only text files there

## Using the python scripts

If you want to just create the tables all dependencies should be part of the standard python libs
dscgraphs.py depends on matplotlib and numpy (doesn't work at the moment)

Once the text logs are in a folder, open dscmsg.py and interact with the CLI

## Config files

If you want to make a table, dscmsg requires you create a config file for your settings before continuing
they are essentially JSON files

If the program gives you a warning about old config files, you can either delete them and make new ones, or open the file in a text editor and append an entry into the JSON list that looks same as *path*

## Shoutouts
Lily for helping me with the datetime module
Yarin for keeping my sanity and helping with like everything
