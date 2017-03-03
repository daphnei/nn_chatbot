from bs4 import BeautifulSoup as BS
import Util
def clean_story(file_name):

	print('Processing story ' + file_name)
	# extract the basic data out of html flags
	with open(file_name) as f:
		soup = BS(''.join(f.readlines()), 'html.parser')

	title = soup.find_all('p')[0].text

	parser = Util.Parser()
	parser.skip_non_empty_attrs = True
	parser.skip_pages = True
	story = parser.parse(soup.find_all('p')).get_text()

	return title, story
