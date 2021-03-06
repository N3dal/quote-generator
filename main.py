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
        quotes = json.load(url)

    return [quote["text"] for quote in quotes]


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


def create_cache_file(quotes: list):
    """create cache file,
    use it also for update cache file."""

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
        quotes = get_api_data()

        # now create cache:
        create_cache_file(quotes)

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


def get_user_input():
    """get input from the user and lower and strip it."""

    POINTER = ">>> "
    return input(POINTER).lower().strip()


def repl():
    """an interactive mode for quote-generator."""

    global ANIMATION_STATE

    # some of commands that kill the repl, simply out for exit from the interactive mode.
    KILL_REPL = ("exit", "quit", "q")

    while (user_input := get_user_input()) not in KILL_REPL:

        if user_input == "clear":
            clear()
        elif user_input == "print":
            random_quote = get_random_quote()
            print(random_quote)
        elif user_input == "update":
            # update quote-cache file.
            pass


def get_random_quote():
    """get random quote from the quote cache file or the api."""
    global ANIMATION_STATE

    # first start the animation.
    animation_task = Thread(target=animation)
    animation_task.start()

    quotes = get_quotes()

    # kill the animation now, after we get our api data.
    ANIMATION_STATE = False

    # now get random from the quotes.
    random_quote = choice(quotes).strip('\n')

    return random_quote


def main():

    # first get the user args.
    user_arguments = get_arguments()

    if user_arguments:
        # start the interactive mode.
        repl()

    else:
        random_quote = get_random_quote()

        print("Today Quote:")
        print(f'"{random_quote}"')


if __name__ == "__main__":
    main()
