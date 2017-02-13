#!/bin/sh

# Where the raw data is saved.
raw_data_dir='twitter_data_dir'
# where the processed data is saved
data_dir='twitter_processed_data_dir'
# Where the model (and checkpoints) are saved
train_dir='checkpoints'

# What fraction of q-a pairs should be witheld for test time
num_test=7265

# argument indication what action this script should perform
action=$1

case $action in
	get_data)
		mkdir $raw_data_dir
		cd $raw_data_dir

		# Get and uncompress the file
		wget -c 'https://raw.githubusercontent.com/Marsan-Ma/chat_corpus/master/twitter_en.txt.gz'
		gunzip twitter_en.txt.gz

		# The above file alternative with ever other line question or answer. Split these into two files.
		sed -n '2~2!p' twitter_en.txt > chat_q.txt
		sed -n '1~2!p' twitter_en.txt > chat_a.txt

		# Split into train and validation sets
		tail -n $num_test chat_q.txt > val_chat_q.txt
		tail -n $num_test chat_a.txt > val_chat_a.txt

        num_train=$(expr $(cat chat_a.txt | wc -l) - $num_test)
		head -n $num_train chat_q.txt > train_chat_q.txt
		head -n $num_train chat_a.txt > train_chat_a.txt
	;;
	train)
        mkdir $data_dir
        mkdir $train_dir
		python translate.py --data_dir $data_dir \
							--train_dir $train_dir \
							--en_vocab_size=40000 \
							--fr_vocab_size=40000 \
							--from_train_data "${raw_data_dir}/train_chat_q.txt"  \
							--to_train_data   "${raw_data_dir}/train_chat_a.txt" \
							--from_dev_data   "${raw_data_dir}/val_chat_q.txt" \
							--to_dev_data     "${raw_data_dir}/val_chat_a.txt"
	;;
	test)
		python translate.py --decode --data_dir $data_dir --train_dir $train_dir
	;;
	*)
		# unknown option
		echo "USAGE: run.sh [get_data|train|test]"
	;;
esac

