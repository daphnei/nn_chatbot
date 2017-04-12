newline_count = 0

buffer = ""
index = 1

import pdb
with open('hca.orig', "r") as in_file:
	for line in in_file:
		buffer = buffer + line
		#print("processing: ")
		#print(line)
		#pdb.set_trace()

		if len(line.strip()) == 0:
			newline_count += 1
		else:
			newline_count = 0

		if newline_count >= 4 :
			if len(buffer.strip()) > 0:
				out_file_name = "hca_%.2d.html" % index
				print("Saving file: " + out_file_name)
				with open(out_file_name, "w") as out_file:
					out_file.write(buffer)
				index += 1

			buffer = ""
			newline_count = 0

