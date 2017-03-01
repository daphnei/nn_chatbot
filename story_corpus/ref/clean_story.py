from bs4 import BeautifulSoup as BS
import re
def clean_story(file_name):

	print('Processing story ' + file_name)
	# extract the basic data out of html flags
	with open(file_name) as f:
		soup = BS(''.join(f.readlines()), 'html.parser')

	title = soup.title.text
	story = ''

	for par in soup.find_all('p'):
		if par.text.strip().startswith('['):
			break
		elif not len(par.attrs) and 'Next:' not in par.text:
			story += par.text

	# remove [1] etc for references
	story = re.sub('\[\w+]', '', story)

	return title, story
