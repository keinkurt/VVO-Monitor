#!/usr/bin/env python3
import argparse
from colorama import Fore, Back, Style, init

import requests
from tabulate import tabulate

from datetime import datetime

init(strip=False)

query_baseurl = 'http://widgets.vvo-online.de/abfahrtsmonitor/Abfahrten.do'
parser = argparse.ArgumentParser()

parser.add_argument('stop')
parser.add_argument('-n', '--num', default=10, help='maximum number of results in the time table')
parser.add_argument('-l', '--lines', nargs='*', help='filter result by specified tram or bus lines')
parser.add_argument('-d', '--destinations', nargs='*', help='filter result by specified destinations')
parser.add_argument('-m', '--mark', nargs='*', help='highlight specified destinations')
args = parser.parse_args()

query = f"{query_baseurl}?hst={args.stop}&lim={args.num}"

response = requests.get(query)

if response.status_code == 200:
    hst_object = response.json()

    if args.lines is not None:
        hst_object = list(filter(lambda x: x[0] in args.lines, hst_object))

    if args.destinations is not None:
        hst_object = list(filter(lambda x: x[1] in args.destinations, hst_object))

    if args.mark is not None:
        for i in range(len(hst_object)):
            now = datetime.now()
            try:
                minute = now.minute + int(hst_object[i][2])
            except:
                minute = now.minute

            if hst_object[i][1] in args.mark and now.hour == 7 and minute > 24 and minute < 45:
                for k in range(len(hst_object[i])):
                    if hst_object[i][2] in ['', '1', '2', '3', '4', '5']:
                        hst_object[i][k] = f"{Back.GREEN}{Fore.BLACK}{hst_object[i][k]}{Style.RESET_ALL}"
                    elif hst_object[i][2] in ['6', '7', '8', '9', '10']:
                        hst_object[i][k] = f"{Back.YELLOW}{Fore.BLACK}{hst_object[i][k]}{Style.RESET_ALL}"
                    else:
                        hst_object[i][k] = f"{Back.RED}{Fore.BLACK}{hst_object[i][k]}{Style.RESET_ALL}"

    print(tabulate(hst_object, headers=["Line", "Destination", "Time"], tablefmt='fancy_grid', maxcolwidths=[None, 15, None]))
else:
    print(f"Something went wrong: {response.reason} ({response.status_code})")
