import urllib2
import csv
from pygtrie import Trie
from pygtrie import PrefixSet
import pickle
import os

def _create_trie():
	tsvs = ["https://www2.census.gov/topics/genealogy/1990surnames/dist.female.first",
			"https://www2.census.gov/topics/genealogy/1990surnames/dist.male.first"]
			# "https://www2.census.gov/topics/genealogy/1990surnames/dist.all.last"]

	# A harded-coded list of exceptions. (names that are more often seen as common noun
	# at the front of sentences.)
	exceptions = ["winter", "grant", "van", "son", "young", "royal", "long", "june", "august", "joy", "young", "aura", "ray", "ok", "harmony", "ha", "sun", "in", "many", "see", "so", "my", "may", "an", "les", "will", "love", "man", "major", "faith"]

	names = []
	for tsv_url in tsvs:
		tsv_file = urllib2.urlopen(tsv_url)

		tabbed = zip(*[line for line in csv.reader(tsv_file, delimiter=' ')])
		names = names + list(tabbed[0])

	names_lower = set()
	for name in names:
		name = name.lower()
		if name not in exceptions:
			names_lower.add(name)

	trie = PrefixSet(names_lower)

	with open('proper_names.pickle', 'w') as outfile:
		pickle.dump(trie, outfile)

	return trie

def get_or_create_proper_names():
	if os.path.exists('proper_names.pickle'):
		with open('proper_names.pickle', 'r') as file:
			return pickle.load(file)
	else:
	 	return _create_trie()


if __name__ == "__main__":
	p = _create_trie()
	print(p.__contains__("daphne"))
	print(p.__contains__("xavier"))
	print(p.__contains__("sally"))
	print(p.__contains__("billy"))
	print(p.__contains__("wxyz"))
	print(p.__contains__("adamrobinson"))
