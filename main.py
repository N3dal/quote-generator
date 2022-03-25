#!/usr/bin/python3
# -----------------------------------------------------------------
# simple app for generate random quotes, on terminal.
#
#
#
# Author:N84.
#
# Create Date:Fri Mar 25 16:02:11 2022.
# ///
# ///
# ///
# -----------------------------------------------------------------

from os import name as OS_NAME
from os import system
from urllib.request import urlopen, Request
import json


def clear():
    """wipe terminal screen."""

    if OS_NAME == "posix":
        # *nix machines.
        system("clear")

    else:
        # windows machines.
        system("cls")


clear()


def get_api_data():
    """return all the quotes from the api."""
    req = Request("https://type.fit/api/quotes",
                  headers={"User-Agent": "Mozilla/5.0"})

    with urlopen(req, timeout=10) as url:
        data = json.load(url)

    return data


def main():

    data = get_api_data()

    print(data)


if __name__ == "__main__":
    main()
