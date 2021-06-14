# Data Analysis and Report Generator

import os
import sys
import requests
import json
import time
import subprocess
import datetime
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
  
  # Populate counter vars 
  for url, stats in analysis_dict.items():
    total_accounts += stats['Total_Accounts']
    total_breaches += stats['Breached_Accounts']
    total_pastes += stats['Pasted_Accounts']
    
  # Print Report Summary
  print("Total URLs Scraped: " + str(len(analysis_dict.keys())))
  print("Total Accounts Scraped: " + str(total_accounts))
  print("Total Accounts Breached: " + str(total_breaches))
  print("Total Accounts Pasted: " + str(total_pastes)) 
  print("-------------------------------------------------------")


  # Print individual URL stats
  for url, stats in analysis_dict.items():
    print("\n------------------")
    print("URL: " + url)
    
    # Get our exposure rate for URL
    if ( stats['Total_Breaches'] + stats['Total_Pastes'] > 0 ) and stats['Total_Accounts'] > 0:
      exposure = float(stats['Total_Breaches'] + stats['Total_Pastes']) / float(stats['Total_Accounts'])
      print("Exposure Rate: " + str(exposure) + "%")
      print("Accounts: " + str(stats['Total_Accounts']))
      print("Breached Accounts: " + str(stats['Total_Breaches']))
      print("Pasted Accounts: " + str(stats['Total_Pastes']))

      
    elif ( stats['Total_Accounts'] ) == 0:
      print("No Accounts Found for URL ")
      
    else: 
      print("Exposure Rate: 0%")
      print("Accounts: " + str(stats['Total_Accounts']))
    
    # Print end of section 
    print("------------------")
  
  
  return
    


def analyze(results_dict):
  
  # Make our main nested dict structure
  analysis_dict = {}
  
  # Pull our dict with filenames as key and accounts listed as values - deprecated
  #account_dict = hibp.get_accounts()
  
  # Make our list of URLs the keys in the nested dict and build keys for nested dict
  for url, accounts in results_dict.items():
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
    analysis_dict[info['URL']]['Total_Accounts'] += 1  
      

  return analysis_dict
    

                  
