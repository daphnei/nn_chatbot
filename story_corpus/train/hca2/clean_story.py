from bs4 import BeautifulSoup as BS
import re
def clean_story(file_name):

	print('Processing story ' + file_name)	

	story = ""
	title = ""

	# extract the basic data out of html flags
	with open(file_name) as f:
		got_title = False
		for line in f:
			if not got_title:
				title = line.strip()
				if len(title) > 0:
					got_title = True
			else:
				story = story + line.strip() + " " 

	return title, story
