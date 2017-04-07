# coding: utf-8

import re

with open('raw_headers.txt', 'r') as f:
    p = open('header.txt', 'w')
    for line in f:
        res = re.match('(?P<key>[^:].+):\s?(?P<value>.+)', line)
        data = "\'" + res.group('key') + "\': " + "\'" + res.group('value') + "\',\n"
        p.write(data)
    p.close()

print('match successfully')
