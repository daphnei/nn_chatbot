from bs4 import BeautifulSoup as BS
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

	for par in soup.find_all('p'):
		if not len(par.attrs) and len(par.contents) and not isinstance(par.contents[0], type(par)):
			story += par.text


	return title, story
