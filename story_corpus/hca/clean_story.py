from bs4 import BeautifulSoup as BS
import re
def clean_story(file_name):

	print('Processing story ' + file_name)	

	story = ""

	# extract the basic data out of html flags
	with open(file_name) as f:
		i = 0
		for line in f:
			if i == 1:
				title = line.strip()
			story = story + line.strip()

	title = title.encode('utf-8')
	story = story.encode('utf-8')

	return title, story
