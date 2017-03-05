from bs4 import BeautifulSoup as BS
import Util
def clean_story(file_name):

	print('Processing story ' + file_name)
	# extract the basic data out of html flags
	with open(file_name) as f:
		soup = BS(''.join(f.readlines()), 'html.parser')

	title = ''
	story = ''

	for h1 in soup.find_all('h1'):
		title += h1.text

	title += ' '
	for h3 in soup.find_all('h3'):
		if not h3.text.startswith('Footnotes'):
			title += h3.text

	parser = Util.Parser()
	parser.skip_non_empty_attrs = True
	parser.skip_pages = True
	story = parser.parse(soup.find_all('p')).get_text()

	return title, story
