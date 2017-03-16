from __future__ import print_function

from bs4 import BeautifulSoup
from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer

import os
import sys

FAKE_DOMAINS = [
	"abcnews",
	"now8news",
	"celebtricity",
	"infowars",
	"naturalnews",
	"libertywritersnews",
	"thelastlineofdefense",
	"prntly",
	"newshounds",
	"americannews",
]

SATIRE_DOMAINS = [
	"clickhole",
	"theonion",
	"newyorker",
]

RECOGNIZED_DOMAINS = [
	"cnn",
	"nytimes",
	"npr",
]

def print_sentiment(ss):
	for k in sorted(ss):
		print('{0}: {1}, '.format(k, ss[k]), end='')

class SentimentAnalysis:
	def __init__(self, soup):
		self.soup = soup

	def _get_sentiment(self, lines):
		sid = SentimentIntensityAnalyzer()
		avg_ss = {
			'neg': 0.0,
			'neu': 0.0,
			'pos': 0.0,
			'compound': 0.0,
		}

		for p in lines:
			ss = sid.polarity_scores(p)
			for k in sorted(ss):
				avg_ss[k] += ss[k]

		for k in avg_ss.keys():
			avg_ss[k] = avg_ss[k] / float(len(lines))

		return avg_ss

	def get_sentiment(self):
		sentences = []

		title = soup.find('h1')
		if title is not None:
			sentences.extend(title.get_text())

		paragraphs = [p.get_text() for p in soup.find_all('p')]
		for p in paragraphs:
			sentences.extend(tokenize.sent_tokenize(p))

		return self._get_sentiment(sentences)

if __name__ == '__main__':
	DATA_DIR = 'data'
	if not os.path.isdir(DATA_DIR):
		print("Missing data directory")

	files = [f for f in os.listdir(DATA_DIR) if os.path.isfile(os.path.join(DATA_DIR, f))]
	files = [f for f in files if not f.startswith('.')]
	image_files = [f for f in files if f.endswith('.images.html')]
	text_files = [f for f in files if f not in image_files]

	fake = []
	satire = []
	recognized = []

	for f in text_files:
		path = os.path.join(DATA_DIR, f)
		soup = None
		with open(path, 'r') as htmlfile:
			soup = BeautifulSoup(htmlfile, 'html.parser')
		sa = SentimentAnalysis(soup)
		ss = sa.get_sentiment()

		for domain in FAKE_DOMAINS:
			if f.find(domain) != -1:
				fake.append((f, ss))

		for domain in SATIRE_DOMAINS:
			if f.find(domain) != -1:
				satire.append((f, ss))

		for domain in RECOGNIZED_DOMAINS:
			if f.find(domain) != -1:
				recognized.append((f, ss))

	print("FAKE NEWS ---------------------")
	for f, ss in fake:
		print("{0}: ".format(f), end='')
		print_sentiment(ss)
		print()		

	print("SATIRE NEWS ---------------------")
	for f, ss in satire:
		print("{0}: ".format(f), end='')
		print_sentiment(ss)
		print()	

	print("RECOGNIZED NEWS ---------------------")
	for f, ss in recognized:
		print("{0}: ".format(f), end='')
		print_sentiment(ss)
		print()	

	#print("{0}: {1}".format(file, ss['compound']))