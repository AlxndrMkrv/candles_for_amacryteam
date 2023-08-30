import pandas as _pd
import os as _os
from io import BytesIO as _BytesIO
from zipfile import ZipFile as _ZipFile
from argparse import ArgumentParser as _ArgumentParser

from dataclasses import dataclass as _dataclass
from collections import deque as _deque
from tempfile import gettempdir as _gettempdir
from urllib import request as _url_request
from enum import Enum as _Enum

from defs import Period as _Period
from ema import convert_to_candlesticks as _convert_to_candlesticks, \
    add_ema as _add_ema

import time
from datetime import datetime, timedelta

data_file_url = "https://perp-analysis.s3.amazonaws.com/interview/prices.csv.zip"


def download_csv_file(url: str = data_file_url) -> str:
    """Download and extract csv file

    Parameters:
        url (str): http link to zipped csv file

    Returns:
        path to extracted csv file
    """
    # Data directory in system temp
    data_dir = f"{_gettempdir()}/candles_for_amacryteam"

    # Create data directory if not present
    if not _os.path.isdir(data_dir):
        _os.mkdir(data_dir)

    # Get csv filename from url
    csv_filename = _os.path.splitext(_os.path.basename(url))[0]

    # Download csv file to data directory if not present
    if csv_filename not in _os.listdir(data_dir):
        content = _url_request.urlopen(url).read()
        # wrap content (zipped data) with BytesIO to imitate 'real' file
        zip_file = _ZipFile(_BytesIO(content))
        zip_file.extractall(data_dir)

    return f"{data_dir}/{csv_filename}"


def parse_csv_file(filename: str) -> _pd.DataFrame:
    """Parse csv file to pandas DataFrame"""


if __name__ == "__main__":
    parser = _ArgumentParser("Test assignment for AmaCryTeam vacancy")
    parser.add_argument("--period", choices=_Period.keys(), default="5m",
                        help="set candlesticks period")
    parser.add_argument("--length", type=int, default=14,
                        help="set EMA length")
    parser.add_argument("--csv", type=str, nargs='?',
                        help="csv file to aggregate. If no file given it will "
                             "be downloaded automatically")
    parser.add_argument("--test", action="store_true", help="run unit tests")
    args = parser.parse_args()

    # Use csv file provided as argument or download the file mentioned in
    # test assignment. Show error if download/unzip failed or invalid file
    # provided
    if args.csv is None:
        try:
            print(f"Trying to download data file from \"{data_file_url}\". "
                  f"Please wait...")
            args.csv = download_csv_file()
        except:
            print(f"Error: failed to download data file or unzip it")
            exit(1)

        # Check if downloaded file exist
        if _os.path.isfile(args.csv):
            print(f"Success! CSV file available at \"{args.csv}\"")
        else:
            print("Something went wrong...")
            exit(1)
    elif not _os.path.isfile(args.csv):
        print(f"Error: CSV file must be provided, \"{args.csv}\" is not a file")
        exit(1)

    # Create pandas DataFrame from downloaded csv file. Use timestamp as index
    def date_parser(string_list):
        return [datetime.fromisoformat(s).timestamp() for s in string_list]

    #df = _pd.read_csv(args.csv, index_col="TS", parse_dates=True)
    df = _pd.read_csv(args.csv, index_col="TS", parse_dates=False)
    df.index = date_parser(df.index)

    # Convert prices into candlesticks with given period
    print()
    ohlc = _convert_to_candlesticks(df, _Period[args.period])

    # Add 'EMA<args.length>' column to candlesticks
    #print(2)
    #_add_ema(ohlc, args.length)

