def clean_story(file_name):

	print('Processing story ' + file_name)	

	story = ""
	title = ""

	# extract the basic data out of html flags
	with open(file_name) as f:
		i = 0
		for line in f:
			if i == 1:
				title = line.strip()
			else:
				story = story + line.strip() + " " 
			i = i + 1

	return title, story
