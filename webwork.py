# Email Webscraper

import os
import sys
import requests
import json
import time
import datetime
import argparse

# Check our input (single URL or file) 
def check_input(URL):
  if "http" or "www" or "://" in URL:
    print("Loaded - Single URL Mode")
    input_type = 1
  elif os.path.isfile(URL):
    print("Loaded - URL List Mode")
    input_type = 2
  else:
    print("URL Input Error")
    input_type = 0
    
  return input_type

# Check that we can reach the URL
def check_URL(URL, input_type):
  url_list = []
  status = 0
  if input_type == 1:
    print("Checking Single URL (" + URL + ")/...")
    url_list.append(URL + "/")
    check_response = requests.get(url_list[0])
    
    if check_response.status_code == 200:
      print("URL Confirmed Reachable!")
      status = 1
    else:
      print("Error Reaching URL")
      print("Error Received: " + str(check_response.status_code))
      status = 0 

  elif input_type == 2:
    print("Checking list of URLs to reach")
    with open(URL) as f:
      url_list = f.readlines()
      url_dictionary = { url : 0 for url in url_list }
    for i in url_list:
      print("Checking " + i + "...")
      check_url = i
      check_response = requests.get(check_url)
    
      if check_response.status_code == 200:
        print("URL Confirmed Reachable!")
        url_dictionary[i] = 1
      else:
        print("Error Reaching URL")
        print("Error Received: " + str(check_response.status_code))
        url_dictionary[i] = 0
      
    if 0 in url_dictionary.values():
      print("Error reaching one or more URLs")
      status = 0
    else:
      print("All URLs Reachable!")
      status = 1
      
  else:
    print("Unable to load URL(s) to check")
  
  return status, url_list

    
def webscraper(URL):
  url_list = []
  input_type = check_input(URL)
  status, url_list = check_URL(URL, input_type)
  
  
  for i in url_list:
    print("Scraping " + i + "/...")
    basename = os.path.basename(i)
    output_file = "account_files/" + basename + "_emails.txt"
    print("Output File: " + output_file)
    os.system("cewl " + i + "/ -n -d 3 -e --email_file " + output_file)
    time.sleep(10)
    print("Waiting on scrape to complete...")
    count = 0
    while (os.stat(output_file).st_size < 1):
          time.sleep(15)
          if count > 20:
            print("Error: no emails found on target URL")
            break
          count+=1


    print("Scraped " + i + " !")

  return
    





