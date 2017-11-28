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

def build_issue_url(args):
    url = "https://api.github.com/repos/" + args.repo[0] + "/issues"
    #If user requested a single issue number, no reason to filter anything else
    if (args.number != None):
        url += "/" + args.number[0]
        return url
    url += "?"
    if (args.state != None):
        url += '&state=' + args.state[0]
    return url

def build_comment_url(args):
    url = "https://api.github.com/repos/" + args.repo[0] + "/issues"
    if (args.number != None):
        url += "/" + args.number[0]
        if (args.comments):
            url += "/comments"

    return url

def parse_args():
    argparser = argparse.ArgumentParser(description="Retrieve issues for a given git repo on either github or gitlab.")
    argparser.add_argument("repo", nargs=1, help="The git repo that you wish to see the issues for.")
    argparser.add_argument("-s", "--state", nargs=1, dest='state', choices=['open', 'closed', 'all'], help="Only show issues with the given state. This is ignored if a number is given.")
    argparser.add_argument("-n", "--number", nargs=1, dest='number', help="The desired issue number to be shown.")
    argparser.add_argument("-c", "--comments", action='store_true', dest='comments', help="Show the comments for this issue as well.")

    args = argparser.parse_args()

    if (args.comments and args.number == None):
        print("Must supply a issue number to recieve comments.")
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
    print("\tUser: " + comment["user"]["login"])
    print("\tCreated at: " + comment["created_at"])
    print("\tUpdated at: " + comment["updated_at"])
    print("\tBody: " + comment["body"])

def print_comments(data):
    for comment in data:
        print_single_comment(comment)
        print("-----------------------------------------------------------------")

if __name__ == "__main__":
    args = parse_args()

    issue_url = build_issue_url(args)
    comment_url = build_comment_url(args)


    try:
        issue_response = urllib.request.urlopen(issue_url)
        issue_data = json.loads(issue_response.read().decode())
        print_results(issue_data)
        if (args.comments):
            comment_response = urllib.request.urlopen(comment_url)
            comment_data = json.loads(comment_response.read().decode())
            print_comments(comment_data)

    except:
        print("Could not find the desired issues for that repo, sorry.")
        exit(0)

