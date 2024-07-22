# HIBP API Integration

import os
import requests
import time
import re

def get_api_key(api_file):
    """
    Read the API key from the provided file.

    Args:
    api_file (str): The path to the file containing the API key.

    Returns:
    str: The API key.
    """
    try:
        with open(api_file, "r") as g:
            api_key = g.readline().strip()
    except IOError:
        print("Error opening HIBP API Key File")
        exit()
    return api_key

def get_accounts():
    """
    Deprecated function to get accounts from account files.
    
    Returns:
    dict: A dictionary with filenames as keys and account lists as values.
    """
    account_dict = {}
    
    if os.path.isdir("account_files"):
        filenames = os.listdir("account_files")
    else:
        print("Error getting account files -- is there an account_files directory?")
        exit()
    
    for filename in filenames:
        accounts = []
        try:
            with open("account_files/" + filename, "r") as h:
                accounts = [line.strip() for line in h]
        except IOError:
            print("Error opening Accounts File")
            exit()

        account_dict[filename] = accounts
    
    return account_dict

def submit_account_breaches(account, api_key_file):
    """
    Submit a request to HIBP API to check for account breaches.

    Args:
    account (str): The email account to check.
    api_key_file (str): The path to the API key file.

    Returns:
    Response: The response from the HIBP API.
    """
    display_account = ("".join((account[:2], re.sub(r'[^@]', r'*', account[1:(account.find('@'))])))) + account[(account.find('@')):]
    req_headers = {'hibp-api-key': get_api_key(api_key_file), 'user-agent': 'Hookshot'}
    breach_url = 'https://haveibeenpwned.com/api/v3/breachedaccount/' + account

    print("Submitting breach request for account: " + display_account)
    breaches_response = requests.get(breach_url, headers=req_headers)
    
    return breaches_response 

def submit_account_pastes(account, api_key_file):
    """
    Submit a request to HIBP API to check for account pastes.

    Args:
    account (str): The email account to check.
    api_key_file (str): The path to the API key file.

    Returns:
    Response: The response from the HIBP API.
    """
    display_account = ("".join((account[:2], re.sub(r'[^@]', r'*', account[1:(account.find('@'))])))) + account[(account.find('@')):]
    req_headers = {'hibp-api-key': get_api_key(api_key_file), 'user-agent': 'Hookshot'}
    paste_url = 'https://haveibeenpwned.com/api/v3/pasteaccount/' + account

    print("Submitting paste request for account: " + display_account)
    pastes_response = requests.get(paste_url, headers=req_headers)
    
    return pastes_response

def check_account_breaches(breach_response, account):
    """
    Check and parse the breach response for a given account.

    Args:
    breach_response (Response): The response from the HIBP API for breaches.
    account (str): The email account checked.

    Returns:
    dict: Information about breaches.
    """
    r = breach_response
    display_account = ("".join((account[:2], re.sub(r'[^@]', r'*', account[1:(account.find('@'))])))) + account[(account.find('@')):]

    breach_info = {
        'num_breaches': 0,
        'breaches': []
    }
    
    if r.status_code == 404:
        print("%s not found in a breach." % display_account)
    elif r.status_code == 200:
        data = r.json()
        print('-------:New Breach Found for: %s' % display_account)
        breach_info['num_breaches'] = len(data)
        breach_info['breaches'] = data
    else:
        data = r.json()
        print('Error: <%s> %s' % (str(r.status_code), data['message']))
        exit()

    return breach_info

def check_account_pastes(paste_response, account):
    """
    Check and parse the paste response for a given account.

    Args:
    paste_response (Response): The response from the HIBP API for pastes.
    account (str): The email account checked.

    Returns:
    dict: Information about pastes.
    """
    r = paste_response
    display_account = ("".join((account[:2], re.sub(r'[^@]', r'*', account[1:(account.find('@'))])))) + account[(account.find('@')):]

    paste_info = {
        'num_pastes': 0,
        'pastes': []
    }
    
    if r.status_code == 404:
        print("%s not found in a paste." % display_account)
    elif r.status_code == 200:
        data = r.json()
        print('-------:New Paste Found for: %s' % display_account)
        paste_info['num_pastes'] = len(data)
        paste_info['pastes'] = data
    else:
        data = r.json()
        print('Error: <%s> %s' % (str(r.status_code), data['message']))
        exit()

    return paste_info

def hibp_checker(keyfile, account_dict):
    """
    Check accounts for breaches and pastes using the HIBP API.

    Args:
    keyfile (str): The path to the API key file.
    account_dict (dict): A dictionary with URLs as keys and account lists as values.

    Returns:
    tuple: A dictionary with account information and a list of URLs with no accounts.
    """
    output_dict = {}
    blank_urls = []

    path = 'output_files/'

    for url, accounts in account_dict.items():
        logfile = "hibp_output.log"
        with open(logfile, "a+") as output_file:
            regurl = re.sub(r'http[s]*\:\/*(www.)*', '', url.strip())
            regurl = re.sub(r'\.[\w]*\/*', '', regurl)
            breachfile = "output_files/" + regurl + "_breached.txt"
            accountfile = "output_files/" + regurl + "_accounts.txt"
            with open(breachfile, "a+") as h:

                if len(accounts) > 1:
                    first_run = 1
                    if os.path.getsize(breachfile) > 0:
                        first_run = 0

                    for account in accounts:
                        display_account = ("".join((account[:2], re.sub(r'[^@]', r'*', account[1:(account.find('@'))])))) + account[(account.find('@')):]

                        if str(account) in open(breachfile).read():
                            print("Found previous breach for " + display_account)
                            output_dict[account] = {'URL': url.strip(), 'Breach_Count': 1, 'Paste_Count': 0}
                        elif ((first_run == 0) and (str(account) in open(accountfile).read()) and (str(account) not in open(breachfile).read())):
                            print("Previously checked " + display_account + " -- no breaches found.")
                            output_dict[account] = {'URL': url.strip(), 'Breach_Count': 0, 'Paste_Count': 0}
                        else:
                            regexp = re.compile(r'[a-zA-Z]+[\w.]*@[\w]*.[a-zA-Z]{2,}')
                            if regexp.search(str(account)):
                                match_account = regexp.search(str(account)).group(0)
                                output_dict[account] = {}

                                time.sleep(1)
                                breach_result = submit_account_breaches(match_account, keyfile)
                                breach_info = check_account_breaches(breach_result, match_account)

                                time.sleep(2)
                                paste_result = submit_account_pastes(match_account, keyfile)
                                paste_info = check_account_pastes(paste_result, match_account)
                                time.sleep(1)

                                output_dict[account] = {
                                    'URL': url.strip(),
                                    'Breach_Count': breach_info['num_breaches'],
                                    'Breach_Detail': breach_info['breaches'],
                                    'Paste_Count': paste_info['num_pastes'],
                                    'Paste_Info': paste_info['pastes']
                                }

                                if breach_info['num_breaches'] >= 1:
                                    h.write(account + "\n")
                else:
                    blank_urls.append(url)

    return output_dict, blank_urls
