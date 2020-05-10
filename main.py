# Main program control

import time
import datetime
import os
import sys
imports argparser
import json
import requests
from hibp import 


def main(argv)

  parser = argparse.ArgumentParser()
  parser.add_argument("key_file", type=str, help="HIBP API Key File")
  parser.add_argument("accounts_file", type=str, help="Account List File") 
  args = parser.parse_args()
  
  
