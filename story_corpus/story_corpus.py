from os import listdir, walk
from os.path import isfile, join
import shelve
from clean_stories import clean_directory

class StoryCorpus(object):
	def __init__(self, path='.', dp_path='stories'):
		self.path = path
		self.db_path = dp_path
		self.topics = 'names'

	# generates db file
	# requires clean_stories to be already run
	def generate_db(self):
		db = shelve.open(self.db_path)

		folderNames = []
		for x in walk(self.path):
			folderPath = x[0]

			if len(folderPath) > 2:
				folderName = folderPath[2:]
				# generate clean txt files
				# clean_directory(folderPath)

				# Parse all the stories into an array
				stories = []
				storyfiles = [f for f in listdir(folderPath) if isfile(join(folderPath, f)) and '.txt' in f]

				for sf in storyfiles:
					path = join(folderPath, sf)
					print("Reading clean story: ", path)
					with open(path, 'r') as file:
						stories.append(file.read())

				db[folderName] = stories
				folderNames.append(folderName)
		db[self.topics] = folderNames

	# returns a list of all the story folders
	def print_main_stories(self):
		db = shelve.open(self.db_path)
		print(db[self.topics])

	# returns a map of storyfolder: list of stories
	def get_stories(self):
		db = shelve.open(self.db_path)
		data = {}

		for topic in db[self.topics]:
			data[topic] = db[topic]

		return data

	# combines all the stories into a giant story array
	def get_flat_data(self):
		story_map = self.get_stories()
		data = []
		for tuple in story_map.items():
			data.append(tuple[1])

		return data

if __name__ == '__main__':
	sc = StoryCorpus()
	# sc.generate_db()
	sc.print_main_stories()
	# print(sc.get_flat_data())