# HIBP API Integration

import os
import sys
import getopt 
import requests
import json
import time
import datetime

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
        print('Breach Check for: %s'%eml)
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



def main(argv):
  accounts_file = ''
  api_key_file = ''
  try:
    opts, args = getopt.getopt(argv,"ha:k:",["accounts=","key="])
    except getopt.GetoptError:
      print 'glaive.py -a <accounts_file> -k <keyfile>'
      sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
         print 'glaive.py -a <accounts_file> -k <key_file>'
          sys.exit()
      elif opt in ("-a", "--acounts"):
         accounts_file = arg
      elif opt in ("-k", "--key"):
         api_key_file = arg

          
          
if __name__ == "__main__":
   main(sys.argv[1:])


