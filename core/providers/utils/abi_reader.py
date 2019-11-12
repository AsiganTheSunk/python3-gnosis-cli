#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import Json Package
import json


class ABIReader:
    def __init__(self):
        pass

    def map(self):
        pass

    def read_from(self, path):
        with open(path) as abi_file:
            d = json.load(abi_file)
            # print(d)
        # return
