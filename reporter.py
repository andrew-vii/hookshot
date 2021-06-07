# Data Analysis and Report Generator

import os
import sys
import requests
import json
import time
import subprocess
import datetime
import argparse

def analyze(results_dict):
  
  # Make our main nested dict structure
  analysis_dict = {}
  
  # Pull our dict with filenames as key and accounts listed as values
  account_dict = hibp.get_accounts()
  
  # Make our list of URLs the keys in the nested dict and build keys for nested dict
  for url, accounts in account_dict.items():
    analysis_dict[url] = {}
    analysis_dict[url]['Breached_Accounts'] = 0
    analysis_dict[url]['Pasted_Accounts'] = 0
    analysis_dict[url]['Total_Accounts'] = 0

  
  # Go through our main dictionary
  for account, info in results_dict.items():
    
    # Increment our breach count for the URL matching the breached account
    if info['Breach_Count'] > 0:
      analysis_dict[info['URL']]['Breached_Accounts'] += 1
      
    if info['Paste_Count'] > 0:
      analysis_dict[info['URL']]['Pasted_Accounts'] += 1
      
    # Increment the total account count for the URL
    analysis_dict[info['Total_Accounts'] += 1
    
    
      

  return
    
    
