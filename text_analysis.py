from __future__ import print_function

from bs4 import BeautifulSoup
from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from HTMLParser import HTMLParser
import os
import sys

def print_sentiment(ss):
	for k in sorted(ss):
		print('{0}: {1}, '.format(k, ss[k]), end='')
	print()

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

		h = HTMLParser()
		paragraphs = [h.unescape(p.get_text()) for p in soup.find_all('p')]
		for p in paragraphs:
			sentences.extend(tokenize.sent_tokenize(p))

		return self._get_sentiment(sentences)

if __name__ == '__main__':
	DATA_DIR = 'data'
	if not os.path.isdir(DATA_DIR):
		print("Missing data directory")

	files = [f for f in os.listdir(DATA_DIR) if os.path.isfile(os.path.join(DATA_DIR, f))]
	image_files = [f for f in files if f.endswith('.images.html')]
	text_files = [f for f in files if f not in image_files]

	for file in text_files:
		path = os.path.join(DATA_DIR, file)
		soup = None
		with open(path, 'r') as htmlfile:
			soup = BeautifulSoup(htmlfile, 'html.parser')
		sa = SentimentAnalysis(soup)
		ss = sa.get_sentiment()
		print("{0}: {1}".format(file, ss['compound']))