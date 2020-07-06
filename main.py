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
  parser.add_argument("ba_keyfile", type=str, help="HIBP API Key File")
  parser.add_argument("accountfile", type=str, help="Account List File") 
  args = parser.parse_args()
  
  while True: 
    # Run HIBP routine 
    hibp.hibp_checker(args.hibp_keyfile, args.accountfile)
    
    # Run BreachAlarm routine - removed after BA removed API access
    #ba.bral_checker(args.ba_keyfile, args.accountfile)
    
    # Set delay
    sleep(43200)
  return 
  
