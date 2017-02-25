#!/bin/sh

root=$1
country=$2
num_start=$3
num_end=$4
name=$5
author=$6

echo "Scraping $num_to_do from $root ."

mkdir -p $root
cd $root

# for i in $(seq 3 39)
for i in $(seq $num_start $num_end)
do
	padded_i=$(printf %02d $i)
	in_file="${root}${padded_i}.htm" 	
	out_file="${root}${padded_i}.html" 	

	# url="http://sacred-texts.com/neu/${country}/${root}/${in_file}"	
	url="http://sacred-texts.com/neu/${country}/${in_file}"	
	echo "Extracting: $i: $url"
	# curl -s $url | nokogiri -e 'puts $_.search('\''body'\'')' > $out_file
	curl -s $url > $out_file
done

echo "{\n\tname: '$name', \n\tauthor: '$author', \n\turl: 'http://sacred-texts.com/neu/${root}/index.htm' \n}" > meta.json
# echo "{\n\tname: '$name', \n\tauthor: '$author', \n\turl: 'http://sacred-texts.com/neu/${country}/${root}/index.htm' \n}" > meta.json
