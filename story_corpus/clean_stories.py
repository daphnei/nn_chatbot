from os import listdir
from os.path import isfile, join
from importlib import import_module
import sys
import nltk.data

def clean_directory(dir_name):
	tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

	onlyfiles = [f for f in listdir(dir_name) if isfile(join(dir_name, f))]

	mod = import_module(dir_name)
	clean_story = getattr(mod, 'clean_story')

	for f in onlyfiles:
		if '.html' in f:
			filePath = dir_name + '/' + f;
			out_name =  filePath.replace('.html', '.txt')
			title, story = clean_story(filePath)

			# remove all new lines from the story
			story = story.replace('\n', ' ')
			story = '\n'.join(tokenizer.tokenize(story))
			story = story.replace('\n""', '"\n"')
			story = story.replace('\n)', ')')


			# output the story
			with open(out_name, mode='w') as f:
				f.write(title.encode('utf-8'))
				f.write('\n')
				f.write(story.encode('utf-8'))


if __name__ == "__main__":
	for arg in sys.argv[1:]:
		print('Processing ' + arg)
		clean_directory(arg)
