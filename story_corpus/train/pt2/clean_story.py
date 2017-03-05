from bs4 import BeautifulSoup as BS
import Util

def clean_story(file_name):

	print('Processing story ' + file_name)
	# extract the basic data out of html flags
	with open(file_name) as f:
		soup = BS(''.join(f.readlines()), 'html.parser')

	title = soup.find('h3').text

	parser = Util.Parser()
	parser.skip_non_empty_attrs = True
	parser.end_on_bracket_beg = True
	parser.skip_pages = True
	story = parser.parse(soup.find_all('p')).remove_digit_references().get_text()

	return title, story
