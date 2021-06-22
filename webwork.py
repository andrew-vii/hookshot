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
def check_input(url):
  if os.path.isfile(url):
    print("Loaded - URL List Mode")
    input_type = 2
  elif "http" or "www" or "://" in url:
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

    # Check our reponse and output the code we get for the URL
    if check_response.status_code == 200 or check_response.status_code == 403 or check_response.status_code == 406:
      print("Received Code " + str(check_response.status_code) + " -- Reachable!")
      url_dict[URL] = check_response.status_code
    else:
      print("Error Reaching URL -- Received Code " + str(check_response.status_code))
      url_dict[URL] = check_response.status_code

  elif input_type == 2:
    print("Checking list of URLs to reach")
    with open(URL) as f:
      url_list = f.readlines()
      url_dict = { url.strip() : 0 for url in url_list }
    for c in url_list:
      i = c.strip()
      time.sleep(0.5)
      print("Checking " + i.strip() + "...")

      # Clean up the url
      check_url = i.strip()

      # Send our GET request with a Windows Firefox UAS (fixes a 406 error)
      check_response = requests.get(check_url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"})

      if check_response.status_code == 200 or check_response.status_code == 403 or check_response.status_code == 406:
        print("Received Code " + str(check_response.status_code) + " -- Reachable!")
        url_dict[i] = check_response.status_code
      else:
        print("Error Reaching URL -- Received Code " + str(check_response.status_code))
        url_dict[i] = check_response.status_code
      
    if 404 in url_dict.values():
      print("Error reaching one or more URLs")
      status = 0
    else:
      print("All " + str(len(url_list)) + " URLs Reachable!\n\n")
      time.sleep(1)
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

  # Set up process dict
  process_dict = {}

  # Run scrapes on target URLs
  for url in url_list:

    # Check URL formatting
    i = url.strip()
    print("\nScraping " + i + "...")

    # Set up our output file
    basename = os.path.basename(i)
    output_file = "account_files/" + basename + "_emails.txt"
    print("Output File: " + output_file)
    newfile = open(output_file, "w+")
    time.sleep(1)
    newfile.close()

    # Set up request parameters
    url_new = i + "/"
    uas = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'

    # Run our scrapes in parallel -- best results with depth at 2 (faster) or 3 (longer, but more thorough)
    scrape_command = "cewl %s --ua %s -n -d 2 -e --email_file %s" % (url_new, uas, output_file)
    process_dict[i] = subprocess.Popen(scrape_command.split(), stdout=subprocess.PIPE)

  # Check states of subprocesses for completion
  proc_states = {}
  proc_complete = 0

  while proc_complete == 0:
    running_scrapes = 0
    for url in url_list:
      i = url.strip()

      if process_dict[i].poll() is None:
        proc_states[i] = 0
        running_scrapes += 1

      else:
        proc_states[i] = 1

    if 0 in proc_states.values():
      proc_complete = 0
      print("Waiting on " + str(running_scrapes) + " scrapes to complete...")
      time.sleep(60)

    else:
      proc_complete = 1
      print("Scrapes complete!")


  for url in url_list:
    
    # Strip line and get the filename
    i = url.strip()
    basename = os.path.basename(i)
    output_file = "account_files/" + basename + "_emails.txt"
      
    # Add URL and accounts scraped to the nested dict
    with open(output_file) as f:

      line_curr = f.read().splitlines()

      # Check for email formatting -- don't add if its a bad match
      regexp = re.compile(r'[a-zA-Z]+[\w.]*@[\w]*.[a-zA-Z]{3}')
      if regexp.search(str(line_curr)):
        output_dict[i] = line_curr

      # If no matching emails, throw a blank string in for accounts found
      else:
        output_dict[i] = '-'


  return output_dict
