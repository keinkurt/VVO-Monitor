#!/usr/bin/env python3
import argparse

import requests
from tabulate import tabulate

query_baseurl = 'http://widgets.vvo-online.de/abfahrtsmonitor/Abfahrten.do'
parser = argparse.ArgumentParser()

parser.add_argument('stop')
parser.add_argument('-n', '--num', default=10)
parser.add_argument('-l', '--lines', nargs='*')
args = parser.parse_args()

query = f"{query_baseurl}?hst={args.stop}&lim={args.num}"

response = requests.get(query)

if response.status_code == 200:
    hst_object = response.json()
    if args.lines is not None:
        hst_object = filter(lambda x: x[0] in args.lines, hst_object)
    print(tabulate(hst_object, headers=["Linie", "Haltestelle", "Abfahrt"], tablefmt='fancy_grid'))
else:
    print(f"Something went wrong: {response.reason} ({response.status_code})")
