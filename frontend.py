import os
import re
import logging
import sys
import json

modeprompt = '''
Please select a mode\n
0 - cumulative - count messages in total before and on this date
1 - non-cumulative - count messages just on this date\n
Mode:\n
'''
time_mode_prompt = '''
Please select a time mode
The Time mode is how the messages are grouped together\n
0 - group by years
1 - group by months
2 - group by days
3 - group by hours\n
Time mode:\n
'''
export_prompt = '''
Select how do you want to export this data:\n
0 - export an interactive HTML page
1 - launch an interactive window (does not save)\n
2 - save output as a csv\n
Export format:\n
'''


class Config:
    def __init__(self, name: str, mode: int, time_mode: int, dest_folder: str, words: bool, export: str) -> None:
        self.name = name  # name of file to be saved
        self.mode = mode  # mode of analysis
        # 0 - count messages (cumulative grouped by time_mode)
        # 1 - count messages (split by time mode)
        self.time_mode = time_mode
        # 0 - years
        # 1 - months
        # 2 - days
        # 3 - hours NOTE: may get a lot of points
        self.dest_folder = dest_folder
        self.words = words
        self.export = export


def call_stack():
    logging.debug(sys._getframe())


def zip_config(config: Config) -> list:
    # get a config file and return a list for saving with json
    out = [
        config.name,
        config.mode,
        config.time_mode,
        config.dest_folder,
        config.words,
        config.export
    ]
    return out


def unzip_config(out: list) -> Config:
    # load a list that contained a config file and return an object
    return Config(out[0], out[1], out[2], out[3], out[4], out[5])


def get_path(query: str):
    # for strings where we don't
    while True:
        got = input(query)
        if os.path.isdir:
            return got
        else:
            logging.info(f'get_path failed with input : {got}')
            print('not a path to a folder, please try again')
            call_stack()


def get_int(query: str) -> int:
    while True:
        got = input(query)
        try:
            return int(got)
        except TypeError:
            logging.info(f'get_int failed with input {got}')
            call_stack()


def get_bool(query: str) -> bool:
    while True:
        got = input(query)
        if got == 'w' or got == 'W':
            return True
        elif got == 'm' or got == 'M':
            return False
        else:
            logging.info(f'get_bool failed with {got}')
            call_stack()


def get_export() -> str:
    confs = ['view', 'html_page']
    while True:
        got = input(f'select how the chart is to be shown\nAvailable export options: {confs}')
        if got in confs:
            return got
        else:
            logging.info(f'get_export failed with {got}')
            call_stack()


def make_config() -> Config:
    mode = get_int(modeprompt)
    time_mode = get_int(time_mode_prompt)
    dest_folder = get_path('Location of logs:\n')
    words = get_bool('Should we count for words or messages?\nW for words\nM for messages\n')
    name = input('Name of file:\n')  # we don't need to clean that one up
    export = get_export()
    new = Config(mode=mode, name=name, time_mode=time_mode, dest_folder=dest_folder, words=words, export=export)
    # out the made list
    out_new = zip_config(new)  # get it into a list so json can take it
    with open(f'{new.name}.dscjson', 'w') as f:
        json.dump(out_new, f)
    return new


def load_config() -> Config:
    wd = os.getcwd()
    out = [f for f in os.listdir(wd) if re.search(r'\.dscjson$', f)]
    if not out:
        logging.info('no file found, creating new one')
        return make_config()
    else:
        # TODO: actually list out files
        got = out[0]
        with open(got, 'r') as f:
            i = json.load(f)
        return unzip_config(i)


def main():
    make_config()


if __name__ == '__main__':
    main()
