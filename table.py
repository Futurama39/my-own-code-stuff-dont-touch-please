import json
import os
import re
import frontend
import pandas as pd
import datetime
import logging
from dateutil.relativedelta import relativedelta
from dateutil import parser


# this program is supposed to get a list of json discord dms
# and an operating mode
# and output a table for the status of that dm


def init(config=None):
    # it is critical for everything in here to have a CONF which is a global, so on import run this func or main()
    # which will also attempt to get it
    global CONF
    if not config:
        CONF = frontend.load_config()
    else:
        CONF = config


def read(fp):
    with open(f"{CONF.dest_folder}{os.sep}{fp}", "r", encoding="UTF-8") as f:
        data = json.load(f)
    return data


def find_json() -> list:
    wd = CONF.dest_folder
    return [f for f in os.listdir(wd) if re.search(r"\.json$", f)]


def first_of(date: datetime.datetime) -> datetime.datetime:
    # get a datetime and on the mode out a start of that day/month/year w/e
    match CONF.time_mode:
        case 0:
            return datetime.datetime(tzinfo=datetime.timezone.utc, year=date.year, month=1, day=1)
        case 1:
            return datetime.datetime(tzinfo=datetime.timezone.utc, year=date.year, month=date.month, day=1)
        case 2:
            return datetime.datetime(tzinfo=datetime.timezone.utc, year=date.year, month=date.month, day=date.day)
        case 3:
            return datetime.datetime(
                tzinfo=datetime.timezone.utc, year=date.year, month=date.month, day=date.day, hour=date.hour
            )


def increment(date: datetime.datetime) -> datetime.datetime:
    match CONF.time_mode:
        case 0:
            return date + relativedelta(years=1)
        case 1:
            return date + relativedelta(months=1)
        case 2:
            return date + relativedelta(days=1)
        case 3:
            return date + relativedelta(hours=1)


def date_lies_in(datestart: datetime.datetime, check: datetime.datetime) -> bool:
    # check if the date lies between datestart and the increment
    top = increment(datestart)
    if datestart <= check < top:
        return True
    else:
        return False


def sort_msg(message: dict):
    return message["timestamp"]


def create_line(file: dict) -> pd.Series:
    name = file["channel"]["name"]
    series = [0]
    file["messages"].sort(
        key=sort_msg
    )  # because of combine.py we work with possibilities of combines being non-contiguous
    first_stamp = file["messages"][0]["timestamp"]
    startdate = first_of(parser.isoparse(first_stamp))
    date_series = [startdate]
    for message in file["messages"]:
        date = parser.isoparse(message["timestamp"])
        # god i love ISO 8601

        # now see how much needs to be added
        if CONF.words:
            num = len(re.findall(r"\w+", message["content"]))
        else:
            num = 1

        # let's see if we can add it to a record or create new one
        if date_lies_in(startdate, date):
            series[-1] += num  # add the number to the last record
        else:
            startdate = first_of(date)
            if date_lies_in(startdate, date):
                date_series.append(startdate)
                if CONF.mode == 0:
                    series.append(num + series[-1])
                    # add past record since we're in cumulative mode
                else:
                    series.append(num)
            else:
                logging.error("date_lies_in after startof assignment failed something has gone wrong")
    col = pd.Series(data=series, index=date_series, name=name)
    return col


def fill_nans(df: pd.DataFrame) -> pd.DataFrame:
    # split up the df into series and then do stuff to them
    if CONF.mode == 1:
        return df.fillna(0)
    else:
        return df.fillna(method="ffill")


def main(config=None, json_loaded=None) -> pd.DataFrame:
    global CONF
    if not config:
        CONF = frontend.load_config()
    else:
        CONF = config
    unopened = find_json()
    # sanity check if we actually have things to find
    if not unopened:
        logging.critical("find_json didn't find anything, aborting...")
        raise FileNotFoundError
    if json_loaded:
        series_list = []
        for file in json_loaded:
            series_list.append(create_line(file).to_frame())
    else:
        series_list = make_df_with_load(unopened)
    out = pd.concat(series_list, axis=1)
    out = out.sort_index()
    out = fill_nans(out)
    return out


def make_df_with_load(unopened):
    serieslist = []
    for f in unopened:
        # first we create a (n,1) series and then
        # we concat it into 'frame' at the end
        file = read(f)
        serieslist.append(create_line(file).to_frame())
    return serieslist


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    print(main())
