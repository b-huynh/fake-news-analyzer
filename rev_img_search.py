import json
import os
import pprint
import sys
from urllib.parse import urlparse

from nltk.metrics import *

curl_command = """curl -X POST -H "Content-Type: application/json" -d '{"image_url":"%s"}' http://localhost:5000/search"""

if len(sys.argv) != 2:
	print("1 URL Argument only")
	sys.exit(1)

url = sys.argv[1]
hostname = urlparse(url).hostname
hostname = hostname.split(".")
if len(hostname) == 2:
	hostname = '.'.join(hostname[0:])
elif len(hostname) == 3:
	hostname = '.'.join(hostname[1:])
elif len(hostname) == 4:
	hostname = '.'.join(hostname[2:])
else:
	print("Weird link... can't determine root domain name")
	sys.exit(1)

exec_command = curl_command % url
rev_img_results = os.popen(exec_command).read()
parsed = json.loads(rev_img_results)
links = parsed['links']
titles = parsed['titles']

# Remove search link
to_remove = []
for i in links:
	if i.startswith('/'):
		to_remove.append(i)
for l in to_remove:
	links.remove(l)

print("Links ---------------------------")
pprint.pprint(links, depth=1)
print()
print("Titles ---------------------------")
pprint.pprint(titles)
print()

website_id = None
for i in range(0, len(links)):
	if links[i].find(hostname) != -1:
		website_id = i

orig_title = titles[website_id] if website_id is not None else titles[0]
if orig_title in titles:
	titles.remove(orig_title)

# Avg edit distance for title
avg_distance = 0
sum_same_title = 0
for t in titles:
	dist = edit_distance(orig_title, t)
	avg_distance += dist
	if dist == 0:
		sum_same_title += 1
avg_distance = avg_distance / len(titles)

print("Using Root Domain: ", hostname)
#print("Original Link: ",links[website_id] if orig_title )
print("Original Title: ", orig_title)
print("Average Edit Distance: %.2f" % avg_distance)
print("Count Same Title: ", sum_same_title)