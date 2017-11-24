#!/usr/bin/python3

import urllib.request, json
import sys, argparse

def build_url(args):
    url = "https://api.github.com/repos/"+args.owner[0]+"/"+args.repo[0]+"/issues"
    return url

#Getting user, repo, desired issue statuses
argparser = argparse.ArgumentParser(description="Retrieve issues for a given git repo on either github or gitlab.")
argparser.add_argument("-r", "--repo", nargs=1, required=True)
argparser.add_argument("-o", "--owner", nargs=1, required=True)
argparser.add_argument("-s", "--state", nargs='+')

args = argparser.parse_args()


url = build_url(args)

response = urllib.request.urlopen(url)
data = json.loads(response.read().decode())[0]
print(data)

