# interact with the DCE a whole ton and handle all the things to just run it over CI/CD
import subprocess
import json
import os
import table
import frontend
import pandas as pd
from typing import List

TOKENLOC = "token.txt"
CONFIGS = "configs.json"

# for the post process move, leave empty if no move desired
DEST = "D:/dmvis/"

with open(TOKENLOC, "r") as f:
    TOKEN = f.read()


# load a list from created tracked_dms.json
def load_cfgs(fp: str = "tracked_dms.json") -> list:
    with open(fp, "r") as f:
        lst = json.load(f)
    return lst


# load a dm from DCE, dce will save this to ./logs
def load_dm(id: int) -> None:
    ret = subprocess.run(
        f"DiscordChatExporter.Cli export -t {TOKEN} -c {id} -f Json -o .{os.sep}logs{os.sep}%c.json", shell=True
    )


def main():
    to_load = load_cfgs()
    # load all the individual ids
    load = input("Download the files? (y/n).\nPick no if you're rerunning the program because of problems\n")
    load = load == "y"
    if load:
        for i in to_load:
            for j in i:
                load_dm(j)
    # now we should have a dir of just logs properly combined so safe to run table for each log we have
    with open(CONFIGS) as f:
        cfglist = json.load(f)
    for i, conf in enumerate(cfglist):
        conf = frontend.unzip_config(conf)
        # load additions to memory here because now we can do addition on them
        table.init(conf)
        alldms = []
        for lst in to_load:
            row = []
            for item in lst:
                row.append(table.read(f"{item}.json"))
            while len(row) != 1:
                row[0]["messages"] += row[-1]["messages"]
                row.pop(-1)
            alldms.append(row[0])

        df = table.main(conf, alldms)
        pd.options.plotting.backend = "plotly"
        fig = df.plot.line()
        # check if html file exists, delete if yes
        write_file = f"out{i}.html"
        if os.path.isfile(write_file):
            os.remove(write_file)
        fig.write_html(write_file)


if __name__ == "__main__":
    main()
