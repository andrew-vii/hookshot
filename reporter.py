# Data analysis and consolidated output 

import os
import sys
import requests
import json
import time
import subprocess
import datetime
import argparse

# Check our input (single URL or file) 
def check_input(URL):
  if os.path.isfile(URL):
    print("Loaded - URL List Mode")
    input_type = 2
  elif "http" or "www" or "://" in URL:
    print("Loaded - Single URL Mode")
    input_type = 1
  else:
    print("URL Input Error")
    input_type = 0
    
  return input_type











