# BreachAlarm API Integration

import os
import sys
import requests
import json
import time
import datetime
import argparse


# Open Breachalarm API Key file and read in API Key value 
def get_api_key(api_file):
  try:
    g = open(api_file,"r")
    api_key = g.readline().strip()
  
  except IOError:
    print("Error opening BreachAlarm API Key File")
    exit()
    
  else:
    print("Unknown Error")
    exit() 
  
  return api_key


def get_accounts(account_file):
  acounts = []
  try:
    h = open(account_file,"r")
    
  except IOError:
    print("Error opening Accounts File")
    exit()
    
  else:
    print("Unknown Error")
    exit() 
    
  for line in h:
    accounts.append(line.strip())
  
  return accounts

def submit_account_breaches(account):
  
  # Set up payload with our API key and distinctive UAS
  payload = {'Api-key': get_api_key(api_key_file),
             'user-agent': 'Bulwark Cybersecurity'
            }
  
  # Set URL for account breaches
  breach_url = 'https://breachalarm.com/api/v1/breachedemails/' + account
  
  # Submit our GET request
  breaches_response = requests.get(submit_url, params=payload)
  
  return breaches_response 
 
  
def check_account_breaches(breach_response):
  
  r = breach_response
  
  breach_info = {
    breaches: []    
  }
  
  # Checking for breaches 
  if r.status_code == 404:
        print("%s not found in a breach."%eml)
    elif r.status_code == 200:
        data = r.json()
        print('Breach Found for: %s'%eml)
        for d in data:
            #   We only really want the name and date of the breach
            count = d['count']
            breach_hist = d['breach_history']
            breach_info['breaches'].append(count + " - " + breach_hist)
            
    else:
        data = r.json()
        print('Error: <%s>  %s'%(str(r.status_code),data['message']))
        exit()
        
  return breach_info

def bral_checker(keyfile, accountfile):
  
  # Set up logfile 
  logfile = "breachalarm_accountlog" + str(datetime.datetime.now()) + ".log"
  output_file = open(logfile,"a+")
  
  # Get accounts
  account_list = get_accounts(args.accounts_file)
  
  # Submit each account for pastes and breaches
  for account in account_list:
    sleep(1)
    breach_result = submit_account_breaches(account)
    sleep(2)
    paste_result = submit_account_pastes(account)
    sleep(1)
    
    # Check results
    check_account_breaches(breach_result)
    check_account_pastes(pastes_result)
    
    # Output results to file
    output_file.write("\n:::" + str(datetime.datetime.now()) + ":::\n:::" + account + ":::\n\n" + breach_result + "\n-----------------------\n\n") 

  output_file.close()
  
  return 


