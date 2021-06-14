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
import reporter as reporter


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("hibp_keyfile", type=str, help="HIBP API Key File")
    parser.add_argument("URL", type=str, help="Target URL")
    args = parser.parse_args()

    # Run URL scraper
    account_dict = webwork.webscraper(args.URL)

    # Run HIBP routine
    main_dict = hibp.hibp_checker(args.hibp_keyfile, account_dict)

    # Run analysis
    analysis_dict = reporter.analyze(main_dict)
        
    # Produce report
    reporter.report(analysis_dict)

    # Close 
    print("\n----------------------------------------------")
    print("PROGRAM COMPLETE")
    print("------------------")

    return


if __name__ == "__main__":
    main(sys.argv)
