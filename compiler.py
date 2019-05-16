#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

with open('./scaner.json', 'r') as f:
    SCANER = json.loads(f.read())

print(SCANER)