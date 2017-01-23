#!/usr/bin/env python3

import argparse
from time import sleep
from features import *

def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default='localhost',
        help="The host ip of the controller")
    parser.add_argument("-t", "--stime", type=int, default=5,
        help="The interval time between requests")
    parser.add_argument("-c", "--count", type=int, default=100,
        help="The number of databases created")
    parser.add_argument("-r", "--rounds", type=int, default=500,
        help="The number of flow requests")
    parser.add_argument("-p", "--prefix", type=str, default="local",
        help="The directory to save databases and figures")
    parser.add_argument("-s", "--save",  action="store_true",
        help="Save the graphics")

    return parser.parse_args()


def main():
    args = parseargs()
    host   = args.host
    stime  = args.stime
    count  = args.count
    rounds = args.rounds
    prefix = args.prefix
    save   = args.save

    for index in range(1, count+1):
        compute_features(index, host, stime, rounds, prefix, save)


if __name__ == '__main__':
    main()
