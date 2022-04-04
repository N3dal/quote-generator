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
from os import listdir
from os import getcwd
from urllib.request import urlopen, Request
import json
from random import choice
from threading import Thread
from time import sleep as delay
from itertools import cycle

URL = "https://type.fit/api/quotes"

# use this for stop the animation.
ANIMATION_STATE = True

CACHE_FILE_NAME = ".quotes.txt"


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

    global ANIMATION_STATE

    CHARS = ('\\', '-', '/', '|')

    # make a cycle object.
    CHARS = cycle(CHARS)

    for char in CHARS:
        if not ANIMATION_STATE:
            break

        print(char, end='\r')
        delay(85e-3)


def create_cache():
    """save the quotes into file."""

    dirs_and_files = listdir(getcwd())

    if CACHE_FILE_NAME not in dirs_and_files:
        with open(f"{getcwd()}/{CACHE_FILE_NAME}", "w") as cache_file:
            for line in get_api_data():
                cache_file.write(line["text"])
                cache_file.write('\n')


def update_cache():
    """update cache file from the api."""
    with open(f"{getcwd()}/{CACHE_FILE_NAME}", "w") as cache_file:
        for line in get_api_data():
            cache_file.write(line["text"])
            cache_file.write('\n')


def main():

    global ANIMATION_STATE

    # first start the animation.
    animation_task = Thread(target=animation)
    animation_task.start()
    cache()
    quotes = get_api_data()

    # kill the animation now, after we get our api data.
    ANIMATION_STATE = False

    # now get random from the quotes.
    random_quote = choice(quotes)

    # notice that the list element that randomly been choose,
    # is in fact a dictionary and the key is always: "text".

    print("Today quote: ")
    print(random_quote["text"])


if __name__ == "__main__":
    main()
