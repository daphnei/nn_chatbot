from os import listdir
from os.path import isfile, join
import sys

import btf.parser as btfparser
import efft.parser as efftparser
import eft.parser as eftparser
import lasi.parser as lasiparser
import meft.parser as meftparser
import mfli.parser as mfliparser
import prwe.parser as prweparser
import pt1.parser as pt1parser
import pt2.parser as pt2parser
import sfft.parser as sfftparser
import swc1.parser as swc1parser
import wfb.parser as wfbparser

def getParser(dir_name):
	if 'btf' == dir_name:
		return btfparser.StoryParser()
	if 'efft' == dir_name:
		return efftparser.StoryParser()
	if 'eft' == dir_name:
		return eftparser.StoryParser()

def clean_story(parser, file_name, out_name, remove_new_lines = False):
	print('Processing story ' + file_name)
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
			clean_story(getParser(dir_name), filePath, filePath.replace('.html', '.txt'), remove_new_lines)


if __name__ == "__main__":
	for arg in sys.argv[1:]:
		print('Processing ' + arg)
		clean_directory(arg, False)
