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
    argparser.add_argument("-r", "--repo", nargs=1, required=True, dest='repo')
    argparser.add_argument("-o", "--owner", nargs=1, required=True, dest='owner')
    argparser.add_argument("-s", "--state", nargs=1, dest='state', choices=['open', 'closed', 'all'])
    argparser.add_argument("-n", "--number", nargs=1, dest='number')

    args = argparser.parse_args()

    return args

def print_single_issue(issue):
    print("-----------------------------------------------------------------")
    print("Title: " + issue["title"])
    print("State: " + issue["state"])
    print("Number: {}".format(issue["number"]))
    print("User: " + issue["user"]["login"])
    print("Created at: " + issue["created_at"])
    print("Updated at: " + issue["updated_at"])
    print("Body: " + issue["body"])

def print_results(data):
    #Only a single issue returned, not an array of issues
    if (args.number != None):
        print_single_issue(data)
        print("-----------------------------------------------------------------")
    else:
        for issue in data:
            print_single_issue(issue)
        print("-----------------------------------------------------------------")

if __name__ == "__main__":
    args = build_arg_parser()
    url = build_url(args)

    try:
        response = urllib.request.urlopen(url)
    except:
        print("Could not find the desired issues for that repo, sorry")
        exit(0)

    data = json.loads(response.read().decode())

    print_results(data)
