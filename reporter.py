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

def report(analysis_dict, output_file):
  
  report_out = ''
  
  # Print report header
  report_out += "\n-------------------------------------------------------"
  report_out += "\nHOOKSHOT Breach/Paste Report Analysis"
  report_out += "\n------------------"
  
  # Set up counter vars
  total_accounts = 0
  total_breaches = 0
  total_pastes = 0
  total_uniques = 0
  
  # Populate counter vars 
  for url, stats in analysis_dict.items():

    # Get the output files again
    regurl = re.sub(r'http[s]*\:\/*(www.)*', '', url.strip())
    regurl = re.sub(r'\.[\w]*\/*', '', regurl)
    breachfile = "output_files/" + regurl + "_breached.txt"
    accountfile = "output_files/" + regurl + "_accounts.txt"

    # Take totals from the size of the files, not just our dictionaries
    with open(accountfile, "r") as c:
      total_accounts += len(c.readlines())
    #total_accounts += stats['Total_Accounts']

    with open(breachfile, "r",) as d:
      total_breaches += len(d.readlines())
    #total_breaches += stats['Breached_Accounts']

    total_pastes += stats['Pasted_Accounts']
    total_uniques += stats['Private_Accounts']
    
  # Print Report Summary
  report_out += "\nTotal URLs Scraped: " + str(len(analysis_dict.keys()))
  report_out += "\nTotal Accounts Scraped: " + str(total_accounts)
  report_out += "\nTotal Accounts Breached: " + str(total_breaches)
  report_out += "\nTotal Accounts Pasted: " + str(total_pastes)
  report_out += "\nTotal Corporate Accounts Exposed: " + str(total_uniques)
  report_out += "\n-------------------------------------------------------\n\n\n"


  # Print individual URL stats
  for url, stats in analysis_dict.items():
    report_out += "\n------------------"
    report_out += "\nURL: " + url

    # Get the output files again
    regurl = re.sub(r'http[s]*\:\/*(www.)*', '', url.strip())
    regurl = re.sub(r'\.[\w]*\/*', '', regurl)
    breachfile = "output_files/" + regurl + "_breached.txt"
    accountfile = "output_files/" + regurl + "_accounts.txt"

    # Grab the count of breaches and accounts from the output files
    with open(accountfile, "r") as e:
      url_accounts = len(e.readlines())
    with open(breachfile, "r",) as f:
      url_breaches = len(f.readlines())

    # Get our exposure rate for URL
    if ( url_breaches > 0 ) and ( url_accounts > 0 ):
      exposure = str(round(100 * float(url_breaches) / float(url_accounts),1))

    #if ( stats['Breached_Accounts'] + stats['Pasted_Accounts'] > 0 ) and stats['Total_Accounts'] > 0:
      #exposure = str(round(100 * float(stats['Breached_Accounts'] + stats['Pasted_Accounts']) / float(stats['Total_Accounts']),1))

      report_out += "\nExposure Rate: " + exposure + "%"
      report_out += "\nAccounts: " + str(url_accounts)
      #report_out += "\nAccounts: " + str(stats['Total_Accounts'])
      report_out += "\nBreached Accounts: " + str(url_breaches)
      #report_out += "\nBreached Accounts: " + str(stats['Breached_Accounts'])
      report_out += "\nPasted Accounts: " + str(stats['Pasted_Accounts'])
      report_out += "\nExposed Corporate Accounts (.org or .gop): " + str(stats['Private_Accounts'])

      
    #elif ( stats['Total_Accounts'] ) == 0:
    elif ( url_accounts == 0):
      report_out += "\nNo Accounts Found for URL "
      
    else: 
      report_out += "\nExposure Rate: 0%"
      report_out += "\nAccounts: " + str(url_accounts)
      #report_out += "\nAccounts: " + str(stats['Total_Accounts'])
    
    # Print end of section 
    report_out += "\n------------------\n"

  # Print full report
  print(report_out)

  # Output report to file
  o = open(output_file, "w")
  o.write(report_out)
  o.close()
  
  return
    

def analyze(results_dict, blank_list):
  
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

  # Then do the same for the blank URLs
  for url in blank_list:
    analysis_dict[url] = {}
    analysis_dict[url]['Breached_Accounts'] = 0
    analysis_dict[url]['Pasted_Accounts'] = 0
    analysis_dict[url]['Total_Accounts'] = 0
    analysis_dict[url]['Private_Accounts'] = 0
  
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
    

                  
