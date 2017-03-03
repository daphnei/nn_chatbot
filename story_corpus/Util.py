import re


def remove_non_ascii(text):
	return ''.join([i if ord(i) < 128 else ' ' for i in text])

class Parser:
	def __init__(self):
		self.end_on_bracket_beg = False
		self.skip_non_empty_attrs = False
		self.end_on_asterix_beg = False
		self.end_on_starts_numeric = False
		self.skip = 0
		self.skip_pages = False
		self.skip_on_bracket_beq = False
		self.text = ''


	def parse(self, content):
		for par in content:
			if self.skip:
				self.skip -= 1
			elif self.end_on_bracket_beg and par.text.strip().startswith('['):
				break
			elif self.skip_on_bracket_beq and par.text.strip().startswith('['):
				continue
			elif self.end_on_asterix_beg and par.text.strip().startswith('*'):
				break
			elif self.end_on_starts_numeric and len(par.text.strip()) and par.text.strip()[0].isdigit():
				break
			elif self.skip_pages and len(par.text.strip()) and isinstance(par.contents[0], type(par)):
				continue # skip
			elif (not len(par.attrs) or not self.skip_non_empty_attrs) and not 'Next:' in par.text:
				self.text += par.text + ' '

		return self

	# removes anything of the form [0-9+] and replaces with a single space
	def remove_digit_references(self):
		self.text = re.sub('\[\d+]', ' ', self.text)
		return self

	def remove_all_references(self):
		self.text = re.sub('\[\w+]', '', self.text)
		return self

	def remove_asterix(self):
		self.text = self.text.replace('*', '')
		return self

	def remove_underscores(self):
		self.text = self.text.replace('_', '')
		return self

	def get_text(self):
		return self.text
