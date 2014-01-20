#!/usr/bin/env python3

import io
import re
import json

import urllib.request
import urllib.parse

from html.parser import HTMLParser
from PIL import Image

class ImageParser(HTMLParser):
	images = []

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.images = []

	def handle_starttag(self, tag, attrs):
		attrs = dict(attrs)
		if tag == "img" and attrs.get("src"):
			self.images.append(attrs["src"])

def normalise_urls(host, file=""):
	"Make urls like 'www.imgur.com' and 'ncss.edu.au' make sense to urllib."
	# magical, standard-non-compliant regex ...
	# please don't kill me -- cyphar
	if re.search(r"^\w+(\.\w+)+", host):
		host = "http://" + host

	if not file:
		return host

	return urllib.parse.urljoin(host, file)

def image_quality(host, url, size=(100, 100)):
	"Calculate the potential 'quality' of an image."
	# Get the image

	url = normalise_urls(host, url)
	request = urllib.request.urlopen(url, None, 1)
	data = request.read()
	request.close()

	# Get the image using virtual IO
	virtio = io.BytesIO(data)
	image = Image.open(virtio)
	image.load()

	# Make a key based on the size of the image
	idealheight, idealwidth = size
	height, width = image.size
	return height + width

def image_exists(host, url):
	"Checks if a linked image actually exists."

	url = normalise_urls(host, url)
	try:
		request = urllib.request.urlopen(url, None, 1)
		request.close()
	except:
		return False

	return True

def find_images(host, string):
	"Get a sorted list of images from some arbitrary html (given the host)."
	h = ImageParser()
	h.feed(string)

	# Convert any relative links to "normalised" links.
	images = [normalise_urls(host, image) for image in h.images if image_exists(host, image)]
	return sorted(images, key=lambda a:image_quality(host, a), reverse=True)

def get_images(url, proxy={}):
	"Get all of the images from a url, sorting them by 'relevance'"
	url = normalise_urls(url)
	request = urllib.request.urlopen(url, None, 1)
	html_str = str(request.read())

	images = find_images(url, html_str)
	return images

def scrape(url, proxy={}):
	"Scrape all images from a url, ignoring errors."
	try:
		return get_images(url, proxy)
	except:
		return None

# Scrape urls for tornado.
def scrape_url(response):
	"Wrap scrape() for tornado usage."
	url = response.get_field("scrape_url")

	if not url:
		return response.write(json.dumps({"error": "404"}))

	images = scrape(url)
	return response.write(json.dumps({"images": images}))

if __name__ == "__main__":
	for web in iter(input, ""):
		print(get_images(web))
