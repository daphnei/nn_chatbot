from bs4 import BeautifulSoup as BS
def clean_story(file_name):

	print('Processing story ' + file_name)
	# extract the basic data out of html flags
	with open(file_name) as f:
		soup = BS(''.join(f.readlines()), 'html.parser')

	title = ''
	story = ''

	paragraphs = soup.find_all('p')

	title = paragraphs[0].text

	for par in paragraphs:
		if not len(par.attrs) and len(par.contents) and not isinstance(par.contents[0], type(par)):
			story += par.text


	return title, story
