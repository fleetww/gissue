#!/usr/bin/python3

import urllib.request, json

url = "https://api.github.com/repos/fleetww/wim/issues"
response = urllib.request.urlopen(url)
data = json.loads(response.read().decode())[0]
print(data)

