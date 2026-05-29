#!/usr/bin/env python3

##############################
# website monitor #
# =============== #
# Monitor the status of a single website or a list of websites from the terminal
# Copyright (c)2026 Ivaylo Vasilev. Released under the MIT License; see LICENSE for details.
# Author: Ivaylo Vasilev
##############################

import requests
from colorama import init, Fore
import argparse
import time
import sys
import os

# up and running state (status code): 200 <= code < 400

# setting up the colors
init(autoreset=True)
GRN = Fore.LIGHTGREEN_EX
RED = Fore.LIGHTRED_EX
YLW = Fore.LIGHTYELLOW_EX
RST = Fore.RESET

# defining a default check interval (seconds)
T = 300.00

parser = argparse.ArgumentParser(prog="wsmon", description="website monitor", epilog="(c)Ivaylo Vasilev")
parser.add_argument("-u", "--url", help="specify URL address to monitor")
parser.add_argument("-f", "--urls-file", help="specify a file with URLs to monitor")
parser.add_argument("-t", "--timer", type=float, default=T, help="specify interval for checking (seconds)")
parser.add_argument("--version", action="version", version="website monitor 0.3", help="show program version and exit")
args = parser.parse_args()


def main():
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    
    print("")
    print("*** website monitor ***")
    print("-----------------------")
    print("")
    
    # prevent setting too short check intervals
    if args.timer >= 30.00:
        timer = args.timer
    else:
        print(f"{YLW}[!]{RST} timer value is too low; using default: {T:.0f} secs")
        timer = T
    
    if args.url:
        url = args.url
        monitor_url(url, timer)
    elif args.urls_file:
        urllist = args.urls_file
        monitor_urls(urllist, timer)


def monitor_url(url, timer):
    print(f"[*] monitoring url: {url}")
    print(f"[*] check interval: {round(timer)} secs")
    print("")

    while True:
        try:
            website_status = get_response(url)

            if website_status == 1:
                print(f"{YLW}[!]{RST} connection error")
                return
            elif website_status == 2:
                print(f"{YLW}[!]{RST} missing schema: try adding http:// or https:// before {url}")
                return
            elif 200 <= website_status < 400:
                print(f"{GRN}[+]{RST} {url}: up")
                time.sleep(timer)
            else:
                print(f"{RED}[-]{RST} {url}: down")
        except KeyboardInterrupt:
            return


def monitor_urls(urllist, timer):
    if not os.path.exists(urllist):
        print(f"{YLW}[!]{RST} file '{urllist}' does not exist")
        return
    
    print("[*] monitoring list of URLs...")
    print(f"[*] check interval: {round(timer)} secs")
    print("")

    urls_list = []
    with open(urllist, "r") as file:
        for line in file.readlines():
            if line.startswith("http"):
                urls_list.append(line.rstrip("\n"))
    
    while True:
        try:
            for url in urls_list:
                website_status = get_response(url)

                if website_status == 1:
                    print(f"{YLW}[!]{RST} connection error")
                    return
                elif 200 <= website_status < 400:
                    print(f"{GRN}[+]{RST} {url}: up")
                else:
                    print(f"{RED}[-]{RST} {url}: down")
            time.sleep(timer)
        except KeyboardInterrupt:
            return


def get_response(url):
    try:
	    r = requests.get(url)
    except requests.exceptions.ConnectionError:
	    return 1
    except requests.exceptions.MissingSchema:
	    return 2
    else:
	    return r.status_code


if __name__ == "__main__":
    main()
