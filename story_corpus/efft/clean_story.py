from bs4 import BeautifulSoup as BS
import Util

def clean_story(file_name):

	print('Processing story ' + file_name)
	# extract the basic data out of html flags
	with open(file_name) as f:
		soup = BS(''.join(f.readlines()), 'html.parser')

	title = ''


	for h1 in soup.find_all('h1'):
		title += h1.text

	parser = Util.Parser()
	parser.end_on_starts_numeric = True
	parser.skip = 1

	story = parser.parse(soup.find_all('p')).remove_asterix().get_text()


	return title, story
