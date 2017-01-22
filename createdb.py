#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 08:34:34 2016

@author: inacio
"""


import os
import sqlite3
import argparse

rootdir=os.path.dirname(os.path.abspath(__file__))


def get_serial():
    with open(os.path.join(rootdir,'serial.txt'),'r') as serial_file:
        serial_number= int(serial_file.readline().rstrip())
    return serial_number


def set_serial(serial):
    with open(os.path.join(rootdir,'serial.txt'),'w') as serial_file:
        serial_file.seek(0,0)
        serial_file.write(str(serial)+'\n')


def create_db():
    schema_db = rootdir+'/ids.sql'
    serial = get_serial()
    db_filename = rootdir+'/%03d.db'%serial
    db_is_new = not os.path.exists(db_filename)
    if db_is_new:
        with sqlite3.connect(db_filename) as conn:
            print('Creating schema: '+db_filename)
            with open(schema_db,'rt') as db:
                schema = db.read()
            conn.executescript(schema)
            print('Schema has been successful created')
            set_serial(serial+1)
    else:
        print('Database alredy exists.')

    return db_filename


def clean_all():
    with open(os.path.join(rootdir,'serial.txt'),'w') as f:
        f.write('1\n')
    print('Deleting all databases')
    [os.remove(os.path.join(rootdir,fdel)) for fdel in os.listdir(rootdir) if fdel.endswith(".db")]


def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d","--delete",help="Delete all databases",
        action="store_true")
    args = parser.parse_args()

    if not args.delete:
        parser.print_help()
        exit(1)
    return args

if __name__=='__main__':
    args = parseargs()
    if args.delete:
        clean_all()

#import time
#import datetime
#ts=time.time()
#st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d')
