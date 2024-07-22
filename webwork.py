# Email Webscraper

import os
import signal
import requests
import time
import subprocess
import re
import random
import urllib3

# Disable URL certificate validation -- fixes a requests error, but use with caution
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def check_input(url):
    """
    Check the input type (single URL, file of URLs, or list of URLs).

    Args:
    url (str or list): The URL or file path or list of URLs to check.

    Returns:
    int: The input type (1 for single URL, 2 for file, 3 for list, 0 for error).
    """
    if isinstance(url, list):
        print("Loaded - Blank URL List Mode\n")
        input_type = 3
    elif os.path.isfile(url):
        print("Loaded - URL List Mode\n")
        input_type = 2
    elif "http" in url or "www" in url or "://" in url:
        print("Loaded - Single URL Mode\n")
        input_type = 1
    else:
        print("URL Input Error\n")
        input_type = 0

    return input_type

def check_URL(URL, input_type):
    """
    Check if the URL(s) can be reached.

    Args:
    URL (str or list): The URL or file path or list of URLs to check.
    input_type (int): The input type (1 for single URL, 2 for file, 3 for list).

    Returns:
    dict: A dictionary with URLs as keys and status codes as values.
    """
    url_dict = {}
    if input_type == 1:
        time.sleep(1)
        print(f"Checking Single URL ({URL})...")
        url_dict[URL] = 0
        check_url = URL.strip()

        try:
            check_response = requests.get(check_url, verify=False, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"})
        except requests.exceptions.RequestException as e:
            print("Encountered unknown error manually checking URL.")
            print(f"Will attempt to request via cewl, but you may want to double-check your connection to {check_url}...")

        if check_response.status_code in [200, 403, 406]:
            print(f"Received Code {check_response.status_code} -- Reachable!")
            url_dict[URL] = check_response.status_code
        else:
            print(f"Error Reaching URL -- Received Code {check_response.status_code}")
            url_dict[URL] = check_response.status_code

    elif input_type == 2:
        print("Checking list of URLs to reach...")
        with open(URL) as f:
            url_list = f.readlines()
            url_dict = {url.strip(): 0 for url in url_list}
        for c in url_list:
            i = c.strip()
            time.sleep(0.5)
            print(f"\nChecking {i.strip()}...")

            check_url = i.strip()

            try:
                check_response = requests.get(check_url, verify=False, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"})
            except requests.exceptions.RequestException as e:
                print("Encountered unknown error manually checking URL.")
                print(f"Will attempt to request via cewl, but you may want to double-check your connection to {check_url}...")

            if check_response.status_code in [200, 403, 406]:
                print(f"Received Code {check_response.status_code} -- Reachable!")
                url_dict[i] = check_response.status_code
            else:
                print(f"Error Reaching URL -- Received Code {check_response.status_code}")
                url_dict[i] = check_response.status_code

        if 404 in url_dict.values():
            print("Error reaching one or more URLs")
            status = 0
        else:
            print(f"\nAll {len(url_list)} URLs Reachable!\n")
            time.sleep(1)
            status = 1

    elif input_type == 3:
        print("Re-loading blank URLs..")
        url_dict = {url.strip(): 0 for url in URL}
        status = 1

    else:
        print("Unable to load URL(s) to check")
        status = 0

    return url_dict

def webscraper(URL, depth, timeout):
    """
    Scrape email addresses from the given URL(s).

    Args:
    URL (str or list): The URL or file path or list of URLs to scrape.
    depth (int): The depth for the scraper to follow links.
    timeout (int): The timeout for the scraper processes.

    Returns:
    dict: A dictionary with URLs as keys and lists of scraped email addresses as values.
    """
    output_dict = {}
    url_list = []

    input_type = check_input(URL)

    url_dict = check_URL(URL, input_type)
    url_list = url_dict.keys()

    process_dict = {}

    path = 'output_files'
    if not os.path.exists(path):
        os.makedirs(path)

    for url in url_list:
        i = url.strip()
        print(f"\nScraping {i}...")

        regurl = re.sub(r'http[s]*\:\/*(www.)*', '', url.strip())
        regurl = re.sub(r'\.[\w]*\/*', '', regurl)
        with open(path + "/" + regurl + "_accounts.txt", "a+"):
            pass

        time.sleep(1)

        uas_list = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; KTXN)"
        ]

        uas = random.choice(uas_list)

        scrape_command = f"cewl {i}/ --ua '{uas}' -n --lowercase -d {depth} -e"

        process_dict[i] = subprocess.Popen(scrape_command, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
        time.sleep(1)

    check_time = 10

    proc_states = {}
    proc_complete = 0
    blank_list = []

    while proc_complete < (int(timeout) / check_time):
        running_scrapes = 0

        for url in url_list:
            i = url.strip()

            if process_dict[i].poll() is None:
                proc_states[i] = 0
                running_scrapes += 1
            else:
                proc_states[i] = 1

        if 0 in proc_states.values():
            proc_complete += 1
            print(f"Waiting on {running_scrapes} scrape(s) to complete...")
            time.sleep(check_time)
        else:
            proc_complete = (int(timeout) / check_time)
            print("\nAll Scrapes Complete!\n")

    for url in url_list:
        i = url.strip()

        if proc_states[i] == 0:
            print(f"Killing timed-out scrape on {i}\n")
            os.killpg(os.getpgid(process_dict[i].pid), signal.SIGTERM)
            blank_list.append(i)

    output_dict = {}

    for url, process in process_dict.items():
        i = url.strip()
        subproc_return = process.stdout.read().decode("utf-8")
        sub

proc_return = re.sub('robin@digi.nin', '', subproc_return)

        regexp = re.compile(r'[a-zA-Z]+[\w.]*@[\w]*.[a-zA-Z]{2,}')
        if regexp.search(subproc_return):
            output_dict[i] = regexp.findall(str(subproc_return))

        if len(subproc_return) <= 75:
            output_dict[i] = ''

    for url, accounts in output_dict.items():
        regurl = re.sub(r'http[s]*\:\/*(www.)*', '', url.strip())
        regurl = re.sub(r'\.[\w]*\/*', '', regurl)
        for account in accounts:
            if str(account) not in open(path + "/" + regurl + "_accounts.txt").read():
                with open(path + "/" + regurl + "_accounts.txt", "a+") as g:
                    g.write(account + "\n")

    return output_dict
