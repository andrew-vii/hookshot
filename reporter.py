# Data Analysis and Report Generator

import os
import sys
import requests
import json
import time
import subprocess
import datetime
import re
import argparse
import hibp as hibp

def report(analysis_dict):
  
  # Print report header
  print("-------------------------------------------------------")
  print("HOOKSHOT Breach/Paste Report Analysis") 
  print("------------------")
  
  # Set up counter vars
  total_accounts = 0
  total_breaches = 0
  total_pastes = 0
  total_uniques = 0
  
  # Populate counter vars 
  for url, stats in analysis_dict.items():
    total_accounts += stats['Total_Accounts']
    total_breaches += stats['Breached_Accounts']
    total_pastes += stats['Pasted_Accounts']
    total_uniques += stats['Private_Accounts']
    
  # Print Report Summary
  print("Total URLs Loaded: " str(sum(len(files) for _, _, files in os.walk('account_files')))
  print("Total URLs Scraped: " + str(len(analysis_dict.keys())))
  print("Total Accounts Scraped: " + str(total_accounts))
  print("Total Accounts Breached: " + str(total_breaches))
  print("Total Accounts Pasted: " + str(total_pastes))
  print("Total Corporate Accounts Exposed: " + str(total_uniques))
  print("-------------------------------------------------------\n\n\n")


  # Print individual URL stats
  for url, stats in analysis_dict.items():
    print("\n------------------")
    print("URL: " + url)
    
    # Get our exposure rate for URL
    if ( stats['Breached_Accounts'] + stats['Pasted_Accounts'] > 0 ) and stats['Total_Accounts'] > 0:
      exposure = str(round(100 * float(stats['Breached_Accounts'] + stats['Pasted_Accounts']) / float(stats['Total_Accounts']),1))

      print("Exposure Rate: " + exposure + "%")
      print("Accounts: " + str(stats['Total_Accounts']))
      print("Breached Accounts: " + str(stats['Breached_Accounts']))
      print("Pasted Accounts: " + str(stats['Pasted_Accounts']))
      print("Exposed Corporate Accounts (.org or .gop): " + str(stats['Private_Accounts']))

      
    elif ( stats['Total_Accounts'] ) == 0:
      print("No Accounts Found for URL ")
      
    else: 
      print("Exposure Rate: 0%")
      print("Accounts: " + str(stats['Total_Accounts']))
    
    # Print end of section 
    print("------------------\n")
  
  
  return
    

def analyze(results_dict):
  
  # Make our main nested dict structure
  analysis_dict = {}
  
  # Pull our dict with filenames as key and accounts listed as values - deprecated
  #account_dict = hibp.get_accounts()
  
  # Make our list of URLs the keys in the nested dict and build keys for nested dict
  for account, info in results_dict.items():
    analysis_dict[info['URL']] = {}
    analysis_dict[info['URL']]['Breached_Accounts'] = 0
    analysis_dict[info['URL']]['Pasted_Accounts'] = 0
    analysis_dict[info['URL']]['Total_Accounts'] = 0
    analysis_dict[info['URL']]['Private_Accounts'] = 0

  
  # Go through our main dictionary
  for account, info in results_dict.items():
    
    # Increment our breach count for the URL matching the breached account
    if info['Breach_Count'] > 0:
      analysis_dict[info['URL']]['Breached_Accounts'] += 1
      
    if info['Paste_Count'] > 0:
      analysis_dict[info['URL']]['Pasted_Accounts'] += 1
      
    # Increment the total account count for the URL
    analysis_dict[info['URL']]['Total_Accounts'] += 1

    # Check and increment .org domain accounts
    reg_ex = re.compile(r'\.[orgp]{3}')
    if (((info['Breach_Count'] > 0) or (info['Paste_Count'] > 0)) and (reg_ex.search(str(account)))):
      analysis_dict[info['URL']]['Private_Accounts'] += 1

  return analysis_dict
    

                  
