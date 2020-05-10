# Main program control

import time
import datetime
import os
import sys
import argparser
import json
import requests
import hibp as hibp


def main(argv)

  parser = argparse.ArgumentParser()
  parser.add_argument("keyfile", type=str, help="HIBP API Key File")
  parser.add_argument("accountfile", type=str, help="Account List File") 
  args = parser.parse_args()
  
  while True: 
    # Run HIBP routine 
    hibp.hibp_checker(args.keyfile, args.accountfile)
    
    # Set delay
    sleep(43200)
  return 
  
