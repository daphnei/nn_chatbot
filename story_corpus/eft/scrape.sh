#!/bin/sh

num_to_do=44

for i in $(seq 1 $num_to_do)
do
	padded_i=$(printf %02d $i)
	
	in_file="efft${padded_i}.htm" 	
	out_file="efft${padded_i}.txt" 	

	url="http://sacred-texts.com/neu/eng/efft/${in_file}"
	echo "Extracting: $i : $url"
	curl -s $url | nokogiri -e 'puts $_.search('\''body'\'')' > $out_file
done


