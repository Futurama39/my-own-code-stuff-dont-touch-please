# Discord DM message tool

Reads discord text channel logs and makes data tables and charts from them  
presumably all versions are a bit broken so just clone from master and hope

## Dependencies
All depend on [Discord Chat Exporter](https://github.com/Tyrrrz/DiscordChatExporter) and getting the logs from there.

For using automation with main.py, the CLI interface is used. In the command launched from the program it is assumed
that the executable is on PATH

Install and  run the program, for your user token [they have a guide](https://github.com/Tyrrrz/DiscordChatExporter/wiki/Obtaining-Token-and-Channel-IDs)

Python specific dependencies:
 ```pandas, python-dateutil, plotly```

And then a bunch of imports that should be in the base python libs

## Setup
First determine which method you want to use:
 - graph.py which can process a folder of downloaded files
 - main.py which can download the specified files form the CLI and then process them

### graph.py
 #### Getting the logs
 Download all the desired channels likely in the GUI. Before downloading,
make sure to set the time mode to ```u``` and the output format to JSON.
Download preferably into an empty folder
 #### Making a config
 If no config is found the program will automatically prompt you to make one
 Supported modes:
 - Time mode: One point can be split by years/months/days/hours
 - Words: Count messages or words
 - Location of the log files
 - Cumulative/non-cumulative
 - Export options: html graph (with plotly)/csv

### main.py
#### Making required files
You'll need to make a few files for the program to read:

 - ```token.txt``` - containing your user token for the program to read (probably protect this file somehow)
 - ```configs.json``` - a list of configs as are created with frontend.py (or manually). 
The program will first load all the dms and then run through all the configs at once.
 - ```tracked_dms.json``` - This file specifies which user IDs/channel IDs are to be downloaded by the CLI.

For getting the right type of ID [consult the chat exporter wiki](https://github.com/Tyrrrz/DiscordChatExporter/blob/master/.docs/Token-and-IDs.md#how-to-get-a-server-id-or-a-server-channel-id).
The file is structured as a list of lists where you may include multiple channel IDs in one nested list
to be combined after downloading. Example:
````
[
 [1],
 [5,2],
 [3],
 [4,6,7]
]
````
In this example the program will try to download channel IDs 1,2,3,4,5,6,7. After being downloaded, channels 2 and 5
will be combined and channels 4 6 and 7 will also be combined.

The names of the series will be the name of the first channel in the list, so in this case the names
of channels 1, 5, 3, 4.


## Using the files as modules
``table`` - Probably the most important. The main function calls for an optional Config class.
If none is provided it will call ``frontend`` to either find or create one. Returns a ``pandas.DataFrame`` of the data.

``frontend`` - Provides most importantly ``make_config()`` and ``load config()``, able to load and make config files.

``graph`` - its ``main()`` takes a ``pandas.DataFrame`` and returns a representation according to the set ``export`` setting in the ``Config`` provided 

``combine`` - A partly obsoleted utility to combine two json records of channels into one. Doesn't work properly.

## old_dscgraphs
This section is for the ``old_dscgraphs`` folders, they have more launch options and such, but they will not be developed. If you're interested you'll be launching dscgraphs.py and following the old readme below
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
