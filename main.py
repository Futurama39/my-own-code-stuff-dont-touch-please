# interact with the DCE a whole ton and handle all the things to just run it over CI/CD 
import subprocess
import json
import combine
import os
import table


TOKENLOC = 'token.txt'
CONFIGS = 'configs.json'

with open(TOKENLOC, 'r') as f:
    TOKEN = f.read()


# load a list from created tracked_dms.txt
def load_cfgs(fp: str = 'tracked_dms.json') -> list:

    with open(fp, 'r') as f:
        lst = json.load(f)
    return lst


# load a dm from DCE, dce will save this to ./logs
def load_dm(id: int) -> None:
    ret = subprocess.run(f'DiscordChatExporter.Cli export -t {TOKEN} -c {id} -f Json -o .{os.sep}logs{os.sep}%c.json', shell=True)
    return ret.stdout




def main():
    to_load = load_cfgs()
    # load all the individual ids
    for i in range(len(to_load) - 1):
        load_dm(to_load[i])
    # and then for the last elem, process all the additions
    for i in to_load[-1]:
        for j in range(1, len(i)):
            combine.main(i[0], i[j])
            # delete second file
            os.remove(f'.{os.sep}logs{os.sep}{i[j]}.json')
    # now we should have a dir of just logs properly combined so safe to run table for each log we have
    with open(CONFIGS) as f:
        cfglist = json.load(f)
    for i, conf in enumerate(cfglist):
        df = table.main(conf)
        fig = df.plot.line()
        # check if html file exists, delete if yes
        write_file = f'{conf.dest_folder}{os.sep}{i}.html'
        if os.path.isfile(write_file):
            os.remove(write_file)
        fig.write_html(write_file)


if __name__ == '__main__':
    main()
