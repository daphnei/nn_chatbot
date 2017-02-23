from HTMLParser import HTMLParser
from os import listdir
from os.path import isfile, join

class StoryParser(HTMLParser):
	title = '';
	story = '';

	processData = False
	ignoreRest = False

	sawTitle = False

	def handle_starttag(self, tag, attrs):
		if tag == 'p' or tag == 'blockquote' or tag == 'h1':
			self.processData = True

	def handle_endtag(self, tag):
		if tag == 'p' :
			self.processData = False

	def handle_data(self, data):
		if data.startswith('*') or 'Footnotes' in data:
			self.ignoreRest = True

		if self.processData and not self.ignoreRest and '[' not in data:
			if self.sawTitle:
					self.story += (data + ' ')
			else:
				self.title = data
				self.sawTitle = True

		self.processData = False


def clean_story(file_name, out_name, remove_new_lines = False):
	# parse
	parser = StoryParser()
	with open(file_name) as f:
		for line in f:
			parser.feed(line)

	# output the story
	with open(out_name, mode='w') as f:
		f.write(parser.title)
		f.write('\n')
		if remove_new_lines:
			f.write(parser.story.replace('\n', ''))
		else:
			f.write(parser.story)

def clean_directory(dir_name, remove_new_lines = False):
	onlyfiles = [f for f in listdir(dir_name) if isfile(join(dir_name, f))]

	for f in onlyfiles:
		if '.html' in f:
			filePath = dir_name + '/' + f;
			clean_story(filePath, filePath.replace('.html', '.txt'), remove_new_lines)

if __name__ == "__main__":
	clean_directory('mfli')