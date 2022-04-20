# HIBP API Integration

import os
import requests
import time
import re


# Open HIBP API Key file and read in API Key value 
def get_api_key(api_file):
  g = open(api_file,"r")
  api_key = g.readline().strip()

  #try:
    #g = open(api_file,"r")
    #api_key = g.readline().strip()
  
  #except IOError:
    #print("Error opening HIBP API Key File")
    #exit()
  
  return api_key

# Deprecated now that webscraper outputs an account dict
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
      h = open("account_files/" + i, "r")

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

  # Display-friendly account
  display_account = ("".join((account[:2], re.sub(r'[^@]',r'*', account[1:(account.find('@'))])))) + account[(account.find('@')):]

  # Set up payload with our HIBP API key and distinctive UAS
  req_headers = {'hibp-api-key': get_api_key(api_key_file),
             'user-agent': 'Hookshot'
            }

  # Set URL for account breaches
  breach_url = 'https://haveibeenpwned.com/api/v3/breachedaccount/' + account

  # Submit our GET request
  print("Submitting breach request for account: " + display_account)
  breaches_response = requests.get(breach_url, headers=req_headers)
  
  return breaches_response 
 
  
def submit_account_pastes(account, api_key_file):

  # Display-friendly account name
  display_account = ("".join((account[:2], re.sub(r'[^@]',r'*', account[1:(account.find('@'))])))) + account[(account.find('@')):]

  # Set up payload with our HIBP API key and distinctive UAS
  req_headers = {'hibp-api-key': get_api_key(api_key_file),
             'user-agent': 'Hookshot'
            }
  
  # Set URL for account pastes
  paste_url = 'https://haveibeenpwned.com/api/v3/pasteaccount/' + account
  
  # Submit our GET request
  print("Submitting paste request for account: " + display_account)
  pastes_response = requests.get(paste_url, headers=req_headers)
  
  return pastes_response


def check_account_breaches(breach_response, account):
  
  r = breach_response

  display_account = ("".join((account[:2], re.sub(r'[^@]',r'*', account[1:(account.find('@'))])))) + account[(account.find('@')):]

  breach_info = {
    'num_breaches': 0,
    'breaches': []
  }
  
  # Checking for breaches 
  if r.status_code == 404:
    print("%s not found in a breach." %display_account)
    
  elif r.status_code == 200:
    data = r.json()
    print('-------:New Breach Found for: %s' %display_account)
    num_breaches = len(data)
    breach_info['num_breaches'] = num_breaches

  else:
    data = r.json()
    print('Error: <%s>  %s'%(str(r.status_code),data['message']))
    exit()

  return breach_info


def check_account_pastes(paste_response, account):
  
  r = paste_response

  display_account = ("".join((account[:2], re.sub(r'[^@]',r'*', account[1:(account.find('@'))])))) + account[(account.find('@')):]
  
  paste_info = {
    'num_pastes': 0,
    'pastes': []
  }
  
  # Checking for pastes 
  if r.status_code == 404:
    print("%s not found in a paste." %display_account)
    
  elif r.status_code == 200:
    data = r.json()
    print('-------:New Paste Found for: %s' %display_account)
    num_pastes = len(data)
    paste_info['num_pastes'] = num_pastes

  else:
    data = r.json()
    print('Error: <%s>  %s'%(str(r.status_code),data['message']))
    exit()

  return paste_info


def hibp_checker(keyfile, account_dict):

  # Create nested dictionary and blank list
  output_dict = {}
  blank_urls = []
  
  # Get accounts - not needed after adding the nested dict output to the webscraper
  #account_dict = get_accounts()

  # Set up filepath
  path = 'output_files/'

  # Submit each account for pastes and breaches
  for url, accounts in account_dict.items():

    # Set up logfile
    logfile = "hibp_output.log"
    output_file = open(logfile,"a+")

    # Set up breached accounts file for each URL
    regurl = re.sub(r'http[s]*\:\/*(www.)*', '', url.strip())
    regurl = re.sub(r'\.[\w]*\/*', '', regurl)
    breachfile = "output_files/" + regurl + "_breached.txt"
    accountfile = "output_files/" + regurl + "_accounts.txt"
    h = open(breachfile, "a+")

    # If there's output for the URL, submit and log
    if len(accounts) > 1:

      # Fix an error related to the first run for adding breaches into a blank list
      first_run = 1
      if (os.path.getsize(breachfile)) > 0:
        first_run = 0

      # Create nested dict as key
      for account in accounts:

        display_account = ("".join((account[:2], re.sub(r'[^@]',r'*', account[1:(account.find('@'))])))) + account[(account.find('@')):]

        # Check if we already have a breach result for this account
        if str(account) in open(breachfile).read():
          print("Found previous breach for " + display_account)
          output_dict[account] = {}
          output_dict[account]['URL'] = url.strip()
          output_dict[account]['Breach_Count'] = 1
          output_dict[account]['Paste_Count'] = 0

        # Future work area - check if we've already checked for a breach on this account
        elif ((first_run == 0) and (str(account) in open(accountfile).read()) and (str(account) not in open(breachfile).read())):
          print("Previously checked " + display_account + " -- no breaches found.")
          output_dict[account] = {}
          output_dict[account]['URL'] = url.strip()
          output_dict[account]['Breach_Count'] = 0
          output_dict[account]['Paste_Count'] = 0

        # Else, the account is new and has not been previously checked for a breach, send it
        else:
          # Double-check on email formatting
          regexp = re.compile(r'[a-zA-Z]+[\w.]*@[\w]*.[a-zA-Z]{3}')

          if regexp.search(str(account)):
            match_account = regexp.search(str(account)).group(0)

            # Add to nested dict
            output_dict[account] = {}

            # Submit account for breaches and check
            time.sleep(1)
            breach_result = submit_account_breaches(match_account, keyfile)
            breach_info = check_account_breaches(breach_result, match_account)

            # Submit account for pastes and check
            time.sleep(2)
            paste_result = submit_account_pastes(match_account, keyfile)
            paste_info = check_account_pastes(paste_result, match_account)
            time.sleep(1)

            # Output breach and paste info to nested dict
            output_dict[account]['URL'] = url.strip()
            output_dict[account]['Breach_Count'] = breach_info['num_breaches']
            output_dict[account]['Breach_Detail'] = breach_info['breaches']
            output_dict[account]['Paste_Count'] = paste_info['num_pastes']
            output_dict[account]['Paste_Info'] = paste_info['pastes']

            # Output info to the breachfile for that account
            if breach_info['num_breaches'] >= 1:
              h.write(account + "\n")

    # Else, if the url didn't have any accounts, add URL to blank list
    else:
      blank_urls.append(url)

    # Close output file
    output_file.close()

  return output_dict,blank_urls


