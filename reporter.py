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



def hibp_checker(keyfile):
  
  
  # Get accounts
  account_dict = get_accounts()
  
  # Submit each account for pastes and breaches
  for url, accounts in account_dict.items():

      # Set up logfile
    logfile = "output_files/" + url + "_accountlog" + str(datetime.datetime.now()) + ".log"
    output_file = open(logfile,"a+")

    for account in accounts:
      time.sleep(1.5)
      breach_result = submit_account_breaches(account, keyfile)
      time.sleep(3)
      paste_result = submit_account_pastes(account, keyfile)
      time.sleep(1.5)

      # Check results
      breach_info = check_account_breaches(breach_result, account)
      paste_info = check_account_pastes(paste_result, account)

      # Output results to file
      output_file.write("\n:::" + str(datetime.datetime.now()) + ":::\n:::" + account + ":::\n\n" + breach_info + "\n\n" + paste_info + "\n-----------------------\n\n")

    output_file.close()
  
  return 









