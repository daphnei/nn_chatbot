from bs4 import BeautifulSoup as BS
import re
def clean_story(file_name):

	print('Processing story ' + file_name)
	# extract the basic data out of html flags
	with open(file_name) as f:
		soup = BS(''.join(f.readlines()), 'html.parser')

	title = ''
	story = ''

	for par in soup.find_all('p'):
		title += par.text

	for block in soup.find_all('blockquote'):
		if block.text.startswith('*'):
			break
		story += block.text

	title = title.encode('utf-8')

	# remove [1] etc for references
	story = story.encode('utf-8')
	story = re.sub('\[\d+]', '', story)
	story = re.sub('\*', '', story)

	return title, story
