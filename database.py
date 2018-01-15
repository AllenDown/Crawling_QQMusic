#! /usr/bin/env python
# -*- coding: utf-8 -*-


import pymongo


def get_sheet(base, sheet):
    client = pymongo.MongoClient('localhost', 27017)
    base = client[base]
    sheet = base[sheet]
    return sheet
