# HIBP API Integration

import os
import sys
import requests
import json
import time
import datetime
import argparse


# Open HIBP API Key file and read in API Key value 
def get_api_key(api_file):
  try:
    g = open(api_file,"r")
    api_key = g.readline().strip()
  
  except IOError:
    print("Error opening HIBP API Key File")
    exit()

  else:
    print("Unknown Error")
    exit()
  
  return api_key


def get_accounts():
  account_dict = {}
  
  if os.path.isdir("account_files"):
    filenames = os.listdir("account_files")
  else:
    print("Error getting account files -- is there an account_files directory?")
    filenames = 0
    exit()
  
  for i in filenames:
    accounts = []

    try:
      h = open(i, "r")

    except IOError:
      print("Error opening Accounts File")
      exit()

    else:
      print("Unknown Error")
      exit()

    for line in h:
      accounts.append(line.strip())
  
    # Update master dict with list of accounts for URL
    account_dict[i] = accounts
  
  return account_dict


def submit_account_breaches(account, api_key_file):
  
  # Set up payload with our HIBP API key and distinctive UAS
  payload = {'hibp-api-key': get_api_key(api_key_file),
             'user-agent': 'Hookshot'
            }
  
  # Set URL for account breaches
  breach_url = 'https://haveibeenpwned.com/api/v3/breachedaccount/' + account
  
  # Submit our GET request
  breaches_response = requests.get(breach_url, params=payload)
  
  return breaches_response 
 
  
def submit_account_pastes(account, api_key_file):
  
  # Set up payload with our HIBP API key and distinctive UAS
  payload = {'hibp-api-key': get_api_key(api_key_file),
             'user-agent': 'Hookshot'
            }
  
  # Set URL for account breaches
  breach_url = 'https://haveibeenpwned.com/api/v3/pasteaccount/' + account
  
  # Submit our GET request
  breaches_response = requests.get(breach_url, params=payload)
  
  return breaches_response


def check_account_breaches(breach_response, account):
  
  r = breach_response
  
  breach_info = {
    'num_breaches': 0,
    'breaches': []
  }
  
  # Checking for breaches 
  if r.status_code == 404:
    print("%s not found in a breach." %account)
  elif r.status_code == 200:
    data = r.json()
    print('Breach Found for: %s' %account)
    num_breaches = len(data)
    for d in data:
        #   We only really want the name and date of the breach
        breach = d['Name']
        breachDate = d['BreachDate']
        breach_info['breaches'].append(breach + " - " + breachDate)

  else:
    data = r.json()
    print('Error: <%s>  %s'%(str(r.status_code),data['message']))
    exit()

  return breach_info


def check_account_pastes(paste_response, account):
  
  r = paste_response
  
  paste_info = {
    'num_pastes': 0,
    'pastes': []
  }
  
  # Checking for pastes 
  if r.status_code == 404:
    print("%s not found in a paste." %account)
  elif r.status_code == 200:
    data = r.json()
    print('Paste Found for: %s' %account)
    num_pastes = len(data)
    for d in data:
        # We only really want the name and date of the paste
        source = d['Source']
        pasteDate = d['Date']
        title = d['Title']
        paste_info['pastes'].append(title + " - " + source + " - " + pasteDate)

  else:
    data = r.json()
    print('Error: <%s>  %s'%(str(r.status_code),data['message']))
    exit()

  return paste_info


def hibp_checker(keyfile):
  
  
  # Get accounts
  account_dict = get_accounts()
  
  # Submit each account for pastes and breaches
  for url, accounts in account_dict.items():

      # Set up logfile
    logfile = url + "_accountlog" + str(datetime.datetime.now()) + ".log"
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


