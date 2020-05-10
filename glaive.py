# HIBP API Integration

import os
import sys
import getopt 
import requests


def get_api_key(api_file):
  
  return api_key

def check_account_breaches(account):
  
  # Set up payload with our HIBP API key and distinctive UAS
  payload = {'hibp-api-key': get_api_key(api_key_file),
             'user-agent': 'Bulwark Cybersecurity'
            }
  
  # Set URL for account breaches
  breach_url = 'https://haveibeenpwned.com/api/v3/breachedaccount/' + account
  
  # Submit our GET with rate limiting avoidance 
  sleep(2) 
  r = requests.get(submit_url, params=payload)
  sleep(1) 
  
  # Checking for breaches 
  if r.status_code == 404:
        print("%s not found in a breach."%eml)
    elif r.status_code == 200:
        data = r.json()
        print('Breach Check for: %s'%eml)
        num_breaches = len(data) 
        for d in data:
            #   Simple info
            breach = d['Name']
            domain = d['Domain']
            breachDate = d['BreachDate']
            sensitive = d['IsSensitive']
            print('Account: %s\nBreach: %s\nSensitive: %s\nDomain: %s\nBreach Date:%s\n'%(eml,breach,sensitive,domain,breachDate))
            #   or to print out the whole shebang comment above and uncomment below
            #for k,v in d.items():
            #    print(k+":"+str(v))
    else:
        data = r.json()
        print('Error: <%s>  %s'%(str(r.status_code),data['message']))
        exit()
  
  return breaches_response 
  
def check_account_pastes(accounts_file): 
  
  return pastes_response


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


