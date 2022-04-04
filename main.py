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
from random import choice
from threading import Thread
from time import sleep as delay
from itertools import cycle

URL = "https://type.fit/api/quotes"


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
    req = Request(URL,
                  headers={"User-Agent": "Mozilla/5.0"})

    with urlopen(req, timeout=3) as url:
        data = json.load(url)

    return data


def animation():
    """create a loading animation on the terminal."""

    CHARS = ('\\', '-', '/', '|')

    # make a cycle object.
    CHARS = cycle(CHARS)

    for char in CHARS:
        print(char, end='\r')
        delay(85e-3)


def main():

    quotes = get_api_data()

    # now get random from the quotes.
    random_quote = choice(quotes)

    # notice that the list element that randomly been choose,
    # is in fact a dictionary and the key is always: "text".

    print("Today quote: ")
    print(random_quote["text"])


if __name__ == "__main__":
    main()
