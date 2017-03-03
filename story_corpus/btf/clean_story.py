from bs4 import BeautifulSoup as BS
import Util

def clean_story(file_name):

	print('Processing story ' + file_name)
	# extract the basic data out of html flags
	with open(file_name) as f:
		soup = BS(''.join(f.readlines()), 'html.parser')

	title = ''

	for par in soup.find_all('p'):
		title += par.text

	parser = Util.Parser()
	parser.end_on_asterix_beg = True

	story = parser.parse(soup.find_all('blockquote')).remove_digit_references().remove_asterix().get_text()

	return title, story
