from bs4 import BeautifulSoup as BS
def clean_story(file_name):

	print('Processing story ' + file_name)
	# extract the basic data out of html flags
	with open(file_name) as f:
		soup = BS(''.join(f.readlines()), 'html.parser')

	story = ''

	paragraphs = soup.find_all('p')

	title = paragraphs[0].text

	for par in paragraphs:
		if par.text.strip().startswith('['):
			break
		elif not len(par.attrs) and 'Next:' not in par.text:
			story += par.text


	return title, story
