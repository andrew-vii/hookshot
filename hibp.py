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


def get_accounts(account_file):
  try:
    h = open(account_file,"r")
    accounts = h.readlines()
    
  except IOError:
    print("Error opening Accounts File")
    exit()
    
  else:
    print("Unknown Error")
    exit() 
    
  return accounts

def submit_account_breaches(account):
  
  # Set up payload with our HIBP API key and distinctive UAS
  payload = {'hibp-api-key': get_api_key(api_key_file),
             'user-agent': 'Bulwark Cybersecurity'
            }
  
  # Set URL for account breaches
  breach_url = 'https://haveibeenpwned.com/api/v3/breachedaccount/' + account
  
  # Submit our GET request
  breaches_response = requests.get(submit_url, params=payload)
  
  return breaches_response 
 
  
def submit_account_pastes(accounts_file): 
  
  # Set up payload with our HIBP API key and distinctive UAS
  payload = {'hibp-api-key': get_api_key(api_key_file),
             'user-agent': 'Bulwark Cybersecurity'
            }
  
  # Set URL for account breaches
  breach_url = 'https://haveibeenpwned.com/api/v3/pasteaccount/' + account
  
  # Submit our GET request
  breaches_response = requests.get(submit_url, params=payload)
  
  return pastes_response


def check_account_breaches(breach_response):
  
  r = breach_response
  
  breach_info = {
    num_breaches: 0,
    breaches: []    
  }
  
  # Checking for breaches 
  if r.status_code == 404:
        print("%s not found in a breach."%eml)
    elif r.status_code == 200:
        data = r.json()
        print('Breach Found for: %s'%eml)
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


def check_account_pastes(paste_response):
  
  r = paste_response
  
  paste_info = {
    num_pastes: 0,
    pastes: []    
  }
  
  # Checking for pastes 
  if r.status_code == 404:
        print("%s not found in a paste."%eml)
    elif r.status_code == 200:
        data = r.json()
        print('Paste Found for: %s'%eml)
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


def main(argv):
  accounts_file = ''
  api_key_file = ''
  
  parser = argparse.ArgumentParser()
  parser.add_argument("key_file", type=str, help="HIBP API Key File")
  parser.add_argument("accounts_file", type=str, help="Account List File") 
  args = parser.parse_args()

  # Set up logfile 
  logfile = "accountlog" + str(datetime.datetime.now()) + ".log"
  output_file = open(logfile,"a+")
  
  # Get accounts
  account_list = get_accounts(args.accounts_file)
  
  # Submit each account for pastes and breaches
  for account in account_list:
    sleep(2)
    breach_result = submit_account_breaches(account)
    sleep(2)
    paste_result = submit_account_pastes(account)
    sleep(1)
    
    # Check results
    check_account_breaches(breach_result)
    check_account_pastes(pastes_result)
    
    # Output results to file
    output_file.write("\n:::" + str(datetime.datetime.now()) + ":::\n:::" + account + ":::\n\n" + breach_result + "\n\n" + paste_result + "\n-----------------------\n\n") 

  output_file.close()
  
if __name__ == "__main__":
   main(sys.argv[1:])


