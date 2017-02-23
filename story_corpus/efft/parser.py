from HTMLParser import HTMLParser

class StoryParser(HTMLParser):
	title = '';
	story = '';

	processData = False
	ignoreRest = False

	sawTitle = False

	def handle_starttag(self, tag, attrs):
		if tag == 'p' or tag == 'blockquote':
			self.processData = True

	def handle_endtag(self, tag):
		if tag == 'p' :
			self.processData = False

	def handle_data(self, data):
		if data.startswith('*'): # skip any asterix
			return

		if self.processData and not self.ignoreRest and '[' not in data:
			if self.sawTitle:
					self.story += (data + ' ')
			else:
				self.title = data
				self.sawTitle = True

		self.processData = False
