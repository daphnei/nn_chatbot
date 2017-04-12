#!/bin/sh

num_to_do=45

for i in $(seq 1 $num_to_do)
do
	padded_i=$(printf %02d $i)
	
	if [ -d "${padded_i}" ]
	then
		echo "${padded_i} already exists."
	else
		in_file="efft${padded_i}.htm" 	
		out_file="efft${padded_i}.txt" 	

		echo "Extracting: $i: http://sacred-texts.com/neu/eng/efft/${in_file}"
		curl -s "http://sacred-texts.com/neu/eng/efft/${in_file}" | nokogiri -e 'puts $_.search('\''body'\'')' > $out_file
	fi
done


