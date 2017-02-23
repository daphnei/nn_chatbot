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
	out_file="${root}${padded_i}.txt" 	

	url="http://sacred-texts.com/neu/${country}/${root}/${in_file}"	
	echo "Extracting: $i: $url"
	curl -s $url | nokogiri -e 'puts $_.search('\''body'\'')' > $out_file
done

echo "{\n\tname: '$4', \n\tauthor: '$5', \n\turl: 'http://sacred-texts.com/neu/${country}/${root}/index.htm' \n}" > meta.json
