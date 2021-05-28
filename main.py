#!/usr/bin/python3
# Main program control

import time
import datetime
import os
import sys
import argparser
import json
import requests
import hibp as hibp
import breachalarm as ba

def main(argv)

  parser = argparse.ArgumentParser()
  parser.add_argument("hibp_keyfile", type=str, help="HIBP API Key File")
  #parser.add_argument("ba_keyfile", type=str, help="HIBP API Key File")
  parser.add_argument("URL", type=str, help="Target URL") 
  args = parser.parse_args()
  
  while True: 
    
    # Run URL scraper
    webwork.webscraper(args.URL)
    
    # Run HIBP routine 
    hibp.hibp_checker(args.hibp_keyfile, args.URL)
    
    # Run BreachAlarm routine - removed after BA removed API access
    #ba.bral_checker(args.ba_keyfile, args.accountfile)
    
    # Set delay
    sleep(1)
  return 
  
