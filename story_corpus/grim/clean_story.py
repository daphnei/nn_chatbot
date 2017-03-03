import Util
def clean_story(file_name):

	print('Processing story ' + file_name)	

	story = ""
	title = ""

	# extract the basic data out of html flags
	with open(file_name) as f:
		got_title = False
		for line in f:
			if not got_title:
				title = line.strip()
				if len(title) > 0:
					got_title = True
			else:
				story = story + line.strip() + " "

	title = Util.remove_non_ascii(title)
	story = Util.remove_non_ascii(story)

	return title, story
