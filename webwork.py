# Email Webscraper

import os
import sys
import requests
import json
import time
import subprocess
import datetime
import argparse
import re

# Check our input (single URL or file) 
def check_input(URL):
  if os.path.isfile(URL):
    print("Loaded - URL List Mode")
    input_type = 2
  elif "http" or "www" or "://" in URL:
    print("Loaded - Single URL Mode")
    input_type = 1
  else:
    print("URL Input Error")
    input_type = 0
    
  return input_type

# Check that we can reach the URL
def check_URL(URL, input_type):
  url_dict = {}
  if input_type == 1:
    time.sleep(1)
    print("Checking Single URL (" + URL + ")...")
    url_dict[URL] = 0
    check_response = requests.get(URL + "/")
    
    if check_response.status_code == 200 or check_response.status_code == 403:
      print("URL Confirmed Reachable!")
      url_dict[URL] = 1
    else:
      print("Error Reaching URL")
      print("Error Received: " + str(check_response.status_code))
      url_dict[URL] = 0

  elif input_type == 2:
    print("Checking list of URLs to reach")
    with open(URL) as f:
      url_list = f.readlines()
      url_dict = { url.strip() : 0 for url in url_list }
    for c in url_list:
      i = c.strip()
      time.sleep(0.5)
      print("Checking " + i.strip() + "...")
      check_url = i.strip()
      check_response = requests.get(check_url)
    
      if check_response.status_code == 200 or check_response.status_code == 403:
        print("URL Confirmed Reachable!")
        url_dict[i] = 1
      else:
        print("Error Reaching URL")
        print("Error Received: " + str(check_response.status_code))
        url_dict[i] = 0
      
    if 0 in url_dict.values():
      print("Error reaching one or more URLs")
      status = 0
    else:
      print("All URLs Reachable!")
      status = 1
      
  else:
    print("Unable to load URL(s) to check")
  
  return url_dict

def webscraper(URL):
  # Set up our list and dict
  output_dict = {}
  url_list = []
  
  # Check whether we received a single URL or a list
  input_type = check_input(URL)
  
  # Check all our URLs to make sure we can reach them 
  url_dict = check_URL(URL, input_type)
  url_list = url_dict.keys()

  # Run scrapes on target URLs
  for url in url_list:
    i = url.strip()
    print("Scraping " + i + "...")
    basename = os.path.basename(i)
    output_file = "account_files/" + basename + "_emails.txt"
    print("Output File: " + output_file)
    url_new = i + "/"

    # Run our scrapes in parallel
    scrape_command = "cewl %s -n -d 3 -e --email_file %s" % (url_new, output_file)
    p = subprocess.Popen(scrape_command.split(), stdout=subprocess.PIPE)

  # Give scrapes time to finish and check output file size for completion
  count = 0
  time.sleep(5)
  while count < 50:
    for url in url_list:
      i = url.strip()
      basename = os.path.basename(i)
      output_file = "account_files/" + basename + "_emails.txt"
      
      # Check output file size to see if our subprocess has completed
      if (os.stat(output_file).st_size < 1):
        time.sleep(10)
        print("Waiting on scrape for " + url + " to complete...")
      count += 1

  # Read into our nested dict and output count of good scrapes
  print("Scrapes complete!")
  good_scrapes = 0
  for url in url_list:
    
    # Strip line and get the filename
    i = url.strip()
    basename = os.path.basename(i)
    output_file = "account_files/" + basename + "_emails.txt"
    
    # Check if we outputted data to the file
    if (os.stat(output_file).st_size < 1):
      good_scrapes += 1
      
    # Add URL and accounts scraped to the nested dict
    with open(output_file) as f:

      line_curr = f.read().splitlines()

      # Check for email formatting -- don't add if its a bad match
      regexp = re.compile(r'[a-zA-Z][\w.]*@[\w]*.[\w]*')
      if regexp.search(str(line_curr)):
        output_dict[i] = line_curr
    

  return output_dict
