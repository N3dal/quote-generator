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
from sys import argv

# Note: this script have a stupid/useless caching mechanism, so plz don't use in your code.
# Simply out this script is useless, and the code to be honest is hurt my eyes, every time that i read it.


# TODO: add REPL like interface that can user interact with it, for example they can generate another quote, or show cache file or update it and other things.
# TODO: ask the users if they want to start program in interact mode by passing [-i] with the command=[./main.py -i].

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


def check_cache():
    """check out if the cache file exist or not."""

    dirs_and_files = listdir(getcwd())

    if CACHE_FILE_NAME in dirs_and_files:
        return True


def update_cache(quotes: list):
    """update/save cache file from the api.
    this will create or update cache file,
    if the file exist this will update it,
    if the file not exist this will create it."""

    with open(f"{getcwd()}/{CACHE_FILE_NAME}", "w") as cache_file:
        for quote in quotes:
            cache_file.write(quote)
            cache_file.write('\n')


def get_cache():
    """return all the quotes that exist in the cache file as list."""

    with open(f"{getcwd()}/{CACHE_FILE_NAME}", "r") as cache_file:
        return cache_file.readlines()


def get_quotes():
    """get the quotes from the api and save them,
    into cache file and then return the quotes."""

    quotes = None

    if check_cache():
        quotes = get_cache()

    else:
        # if the cache file not exist.
        quotes = [quote["text"] for quote in get_api_data()]

        # now create cache:
        update_cache(quotes)

    return quotes


def get_arguments():
    """get the arguments from the user,
    and checkout if the args are exist or not."""

    ARGUMENTS = ('-i',)

    user_arguments = argv[1:]

    for arg in user_arguments:
        if arg not in ARGUMENTS:
            return False

    return user_arguments


def repl():
    """an interactive mode for quote-generator."""


def main():

    global ANIMATION_STATE

    # first get the user args.
    user_arguments = get_arguments()

    if user_arguments:
        # start the interactive mode.
        pass

    # first start the animation.
    animation_task = Thread(target=animation)
    animation_task.start()

    quotes = get_quotes()

    # kill the animation now, after we get our api data.
    ANIMATION_STATE = False

    # now get random from the quotes.
    random_quote = choice(quotes).strip('\n')

    # notice that the list element that randomly been choose,
    # is in fact a dictionary and the key is always: "text".

    print("Today quote: ")
    print(random_quote)


if __name__ == "__main__":
    main()
