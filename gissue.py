#!/usr/bin/python3

import urllib.request, json
import sys, argparse

def build_url(args):
    url = "https://api.github.com/repos/"+args.repo[0]+"/issues"
    #If user requested a single issue number, no reason to filter anything else
    if (args.number != None):
        url += "/" + args.number[0]
        if (args.comments):
            url += "/comments"
        return url
    url += "?"
    if (args.state != None):
        url += '&state=' + args.state[0]
    return url

def parse_args():
    argparser = argparse.ArgumentParser(description="Retrieve issues for a given git repo on either github or gitlab.")
    argparser.add_argument("repo", nargs=1)
    argparser.add_argument("-s", "--state", nargs=1, dest='state', choices=['open', 'closed', 'all'])
    argparser.add_argument("-n", "--number", nargs=1, dest='number')
    argparser.add_argument("-c", "--comments", action='store_true', dest='comments')

    args = argparser.parse_args()

    if (args.comments and args.number == None):
        print("Must supply a issue number to recieve comments")
        exit(1)

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

def print_single_comment(comment):
    print("-----------------------------------------------------------------")
    print("User: " + comment["user"]["login"])
    print("Created at: " + comment["created_at"])
    print("Updated at: " + comment["updated_at"])
    print("Body: " + comment["body"])

def print_comments(data):
    for comment in data:
        print_single_comment(comment)
        print("-----------------------------------------------------------------")

if __name__ == "__main__":
    args = parse_args()
    url = build_url(args)

    try:
        response = urllib.request.urlopen(url)
    except:
        print("Could not find the desired issues for that repo, sorry")
        exit(0)

    data = json.loads(response.read().decode())

    if (args.comments):
        print_comments(data)
    else:
        print_results(data)
