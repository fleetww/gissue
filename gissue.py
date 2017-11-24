#!/usr/bin/python3

import urllib.request, json
import sys, argparse

def build_url(args):
    url = "https://api.github.com/repos/"+args.owner[0]+"/"+args.repo[0]+"/issues"
    #If user requested a single issue number, no reason to filter anything else
    if (args.number != None):
        url += "/" + args.number[0]
        return url
    url += "?"
    if (args.state != None):
        url += '&state=' + args.state[0]
    return url

def build_arg_parser():
    argparser = argparse.ArgumentParser(description="Retrieve issues for a given git repo on either github or gitlab.")
    argparser.add_argument("-r", "--repo", nargs=1, required=True)
    argparser.add_argument("-o", "--owner", nargs=1, required=True)
    argparser.add_argument("-s", "--state", nargs=1)
    argparser.add_argument("-n", "--number", nargs=1)

    args = argparser.parse_args()

    return args


args = build_arg_parser()

url = build_url(args)
print(url)

try:
    response = urllib.request.urlopen(url)
except:
    print("Could not find the desired issues for that repo, sorry")
    exit(0)

#Will only be a single issue if number specified, so in the future we must check
#if the desired number was specified
data = json.loads(response.read().decode())
print(data)

