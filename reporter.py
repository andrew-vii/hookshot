# Data Analysis and Report Generator

import os
import re

def report(analysis_dict, output_file):
    """
    Generate a report based on the analysis dictionary and output it to a file.

    Args:
    analysis_dict (dict): The dictionary containing analysis results.
    output_file (str): The path to the output file where the report will be saved.
    """
    report_out = ''
    
    # Print report header
    report_out += "\n-------------------------------------------------------"
    report_out += "\nHOOKSHOT Breach/Paste Report Analysis"
    report_out += "\n-------------------------------------------------------"
    
    # Set up counter variables
    total_accounts = 0
    total_breaches = 0
    total_pastes = 0
    total_uniques = 0
    
    # Populate counter variables
    for url, stats in analysis_dict.items():
        regurl = re.sub(r'http[s]*\:\/*(www.)*', '', url.strip())
        regurl = re.sub(r'\.[\w]*\/*', '', regurl)
        breachfile = "output_files/" + regurl + "_breached.txt"
        accountfile = "output_files/" + regurl + "_accounts.txt"

        with open(accountfile, "r") as c:
            total_accounts += len(c.readlines())

        with open(breachfile, "r") as d:
            total_breaches += len(d.readlines())

        total_pastes += stats['Pasted_Accounts']
        total_uniques += stats['Private_Accounts']
    
    # Print Report Summary
    report_out += f"\nTotal URLs Scraped: {len(analysis_dict.keys())}"
    report_out += f"\nTotal Accounts Scraped: {total_accounts}"
    report_out += f"\nTotal Accounts Breached: {total_breaches}"
    report_out += f"\nTotal Accounts Pasted: {total_pastes}"
    report_out += f"\nTotal Corporate Accounts Exposed: {total_uniques}"
    report_out += "\n-------------------------------------------------------\n\n\n"

    # Print individual URL stats
    for url, stats in analysis_dict.items():
        report_out += "\n-------------------------------------------------------"
        report_out += f"\nURL: {url}"
        
        regurl = re.sub(r'http[s]*\:\/*(www.)*', '', url.strip())
        regurl = re.sub(r'\.[\w]*\/*', '', regurl)
        breachfile = "output_files/" + regurl + "_breached.txt"
        accountfile = "output_files/" + regurl + "_accounts.txt"

        with open(accountfile, "r") as e:
            url_accounts = len(e.readlines())
        with open(breachfile, "r") as f:
            url_breaches = len(f.readlines())

        if (url_breaches > 0) and (url_accounts > 0):
            exposure = str(round(100 * float(url_breaches) / float(url_accounts), 1))

            report_out += f"\nExposure Rate: {exposure}%"
            report_out += f"\nAccounts: {url_accounts}"
            report_out += f"\nBreached Accounts: {url_breaches}"
            report_out += f"\nPasted Accounts: {stats['Pasted_Accounts']}"
            report_out += f"\nExposed Corporate Accounts (.org or .gop): {stats['Private_Accounts']}"
        elif url_accounts == 0:
            report_out += "\nNo Accounts Found for URL"
        else:
            report_out += "\nExposure Rate: 0%"
            report_out += f"\nAccounts: {url_accounts}"

        report_out += "\n-------------------------------------------------------\n"

    print(report_out)

    with open(output_file, "w") as o:
        o.write(report_out)
    
    return

def analyze(results_dict, blank_list):
    """
    Analyze the results dictionary and return an analysis dictionary.

    Args:
    results_dict (dict): The dictionary containing results.
    blank_list (list): List of URLs with no results.

    Returns:
    dict: The dictionary containing analysis results.
    """
    analysis_dict = {}
    
    for account, info in results_dict.items():
        analysis_dict[info['URL']] = {
            'Breached_Accounts': 0,
            'Pasted_Accounts': 0,
            'Total_Accounts': 0,
            'Private_Accounts': 0
        }

    for url in blank_list:
        analysis_dict[url] = {
            'Breached_Accounts': 0,
            'Pasted_Accounts': 0,
            'Total_Accounts': 0,
            'Private_Accounts': 0
        }
    
    for account, info in results_dict.items():
        if info['Breach_Count'] > 0:
            analysis_dict[info['URL']]['Breached_Accounts'] += 1
        
        if info['Paste_Count'] > 0:
            analysis_dict[info['URL']]['Pasted_Accounts'] += 1
        
        analysis_dict[info['URL']]['Total_Accounts'] += 1

        reg_ex = re.compile(r'\.[orgp]{3}')
        if ((info['Breach_Count'] > 0) or (info['Paste_Count'] > 0)) and reg_ex.search(str(account)):
            analysis_dict[info['URL']]['Private_Accounts'] += 1

    return analysis_dict
