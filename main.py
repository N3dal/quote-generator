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
from urllib.request import urlopen
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


def main():
    pass


if __name__ == "__main__":
    main()
