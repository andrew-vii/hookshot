#!/usr/bin/python3

# Main program control
import os
import sys
import argparse
import hibp as hibp
import webwork as webwork
import reporter as reporter


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("hibp_keyfile", type=str, help="HIBP API Key File")
    parser.add_argument("URL", type=str, help="Target URL")
    parser.add_argument("depth", type=str, help="Cewl Spidering Depth (2 or 3 recommended")
    parser.add_argument("output_file", type=str, help="Output File")
    parser.add_argument("timeout", type=str, help="Webscraper Timeout")
    args = parser.parse_args()

    os.system('clear')
    print("\n----------------------------------------------")
    print("Hookshot Breach Comparison Tool")
    print("v1.1 - Stable")
    print("----------")

    # Run URL scraper
    account_dict = webwork.webscraper(args.URL, args.depth, args.timeout)

    # Run HIBP routine
    main_dict, blank_list = hibp.hibp_checker(args.hibp_keyfile, account_dict)
    
    # Re-run on blank/empty URLs
    deep_dict = {}
    fail_list = []
    # Check if we have blank/missing URLs
    if len(blank_list) > 0:
        # Re-scrape the URLs with more depth and more time for command to complete 
        account_dict = webwork.webscraper(blank_list, args.depth, (int(args.timeout) * 10))
        # Send the new accounts against HIBP
        deep_dict, fail_list = hibp.hibp_checker(args.hibp_keyfile, account_dict)
        # Update the main dict to be analyzed 
        main_dict = main_dict | deep_dict
        

    # Run analysis
    analysis_dict = reporter.analyze(main_dict,blank_list)
        
    # Produce report
    reporter.report(analysis_dict, args.output_file)

    # Close 
    print("\n----------------------------------------------")
    print("PROGRAM COMPLETE")
    print("------------------")

    return


if __name__ == "__main__":
    main(sys.argv)
