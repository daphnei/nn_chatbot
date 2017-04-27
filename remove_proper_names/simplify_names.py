import glob
import os
# from nltk.tokenize import sent_e
import pickle
import nltk
import proper_names
import pdb
import itertools
import zlib
import pdb
import unicodedata
import pickle
from dateutil.parser import parse

def is_date(string):
	try: 
		exceptions = ["sun", "sat"]
 		parse(string)
 		return string not in exceptions
 	except:
		return False

def is_number(s):
 	try:
		v = float(s)
 		return v <= 1700 or  v >= 3000
 	except: # (ValueError, OverflowError):
 		pass
 
 	try:
	 	unicodedata.numeric(s)
 		return True
 	except: #(TypeError, ValueError, OverflowError):
 		pass
 
	return False

def remove_non_ascii(text):
  '''removes any characters outside of the ASCII range from a string '''
  return ''.join([i if ord(i) < 128 else ' ' for i in text])

if __name__ == "__main__":
	'''
       saves the books into a file with CONV_LENGTH sentences (utterances) on each line 
       and sentence tags in between them
    '''

	in_file = "/home/ubuntu/nn_chatbot/seq2seq/scripts/data/books_large_p1.txt" 
	out_file = "/home/ubuntu/nn_chatbot/seq2seq/scripts/data/books_large_p1_simplified.txt" 
	#in_file = "/media/snake/daphne/school/nn_chatbot/big_book_corpus/in_sentences/books_large_p1.txt"
	#out_file = "/media/snake/daphne/school/nn_chatbot/big_book_corpus/in_sentences/books_large_p1_simplified.txt"

	# Simplify the text to only have these many unique names
	NUM_NAMES = 100

	output = ""

	word_tokenizer = nltk.TreebankWordTokenizer()

	proper_names_trie = proper_names.load()

	names_so_far = {}
	dates = set()
	numbers = set()

	line_index = 0
	with open(in_file, 'r') as f_in:
		with open(out_file, 'w') as f_out:
			for line in f_in:
				line_index = line_index + 1
				if line_index <= -1:
					pass 
				else:
					words = line.split(" ")
	
					for i in xrange(0, len(words)):
						word = words[i]
						if word.lower() in proper_names_trie: #and word[0] == word[0].upper():
							# This is a proper name. Check if it is one we have seen before in this text
							replacement_name = "_name_" + str(zlib.adler32(word) % NUM_NAMES)
							words[i] = replacement_name
						elif is_number(word):
							words[i] = "_number_"
							#if word not in numbers:
							#	print("New number: " + word)
							#	numbers.add(word)
						elif is_date(word):
							words[i] = "_date_"
							#if word not in dates:
							#	print("New date: " + word)
							#	dates.add(word)
		
					out_line = " ".join(words)
					f_out.write(out_line)
	
					if line_index%50000==0:
						print("i = " + str(line_index) + ": " + line + " -> " + out_line)
			

	with open("removed_meta.pickle", "w") as f_out:
		pickle.dump((numbers, dates), f_out)

		
