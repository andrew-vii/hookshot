#!/usr/bin/python3

# Main program control

import time
import datetime
import os
import sys
import argparse
import _thread
import json
import requests
import hibp as hibp
import webwork as webwork


# import hibp as hibp
# import breachalarm as ba

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("hibp_keyfile", type=str, help="HIBP API Key File")
    # parser.add_argument("ba_keyfile", type=str, help="HIBP API Key File")
    parser.add_argument("URL", type=str, help="Target URL")
    args = parser.parse_args()

    while True:
        # Run URL scraper
        webwork.webscraper(args.URL)

        # Run HIBP routine
        hibp.hibp_checker(args.hibp_keyfile)

        # Set delay
        time.sleep(1)

        
    return


if __name__ == "__main__":
    main(sys.argv)
