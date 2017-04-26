# dataFile='/media/snake/daphne/school/nn_chatbot/book_corpus_tagged/book_corpus_names_removed/train.txt'
dataFile='/media/snake/daphne/school/nn_chatbot/big_book_corpus/in_sentences/books_large_p1_simplified.txt'

outputDir='/media/snake/daphne/school/nn_chatbot/seq2seq/scripts/train_processed'

inputFile="${outputDir}/input.txt"
inputEncoded="${outputDir}/input.enc"
outputFile="${outputDir}/output.txt"
outputEncoded="${outputDir}/output.enc"

vocabFile="${outputDir}/vocab.tok.txt"
codesFile="${outputDir}/bpe.32000"


# Generate the input and output mappings (input is missing last line, output is missing first)
echo "Splitting text file into input file and output file"
sed '$d' < ${dataFile} > ${inputFile}
sed '1d' < ${dataFile} > ${outputFile}

# Clone Moses
if [ ! -d "${outputDir}/mosesdecoder" ]; then
  echo "Cloning moses for data processing"
  git clone https://github.com/moses-smt/mosesdecoder.git "${outputDir}/mosesdecoder"
fi

# Create character vocabulary (on tokenized data)
# echo "Creating vocabulary on tokenized data."
# ../bin/tools/generate_vocab.py --delimiter " " --max_vocab_size 70000 \
  # < ${dataFile} \
  # > ${vocabFile}
# 

  # Generate Subword Units (BPE)
# Clone Subword NMT
# if [ ! -d "${outputDir}/subword-nmt" ]; then
  # git clone https://github.com/rsennrich/subword-nmt.git "${outputDir}/subword-nmt"
# fi

# learn the bpe
# ${outputDir}/subword-nmt/learn_bpe.py -s 32000 < ${dataFile} > ${codesFile}

# apply the bpe to output and input files
# ${outputDir}/subword-nmt/apply_bpe.py -c ${codesFile} < ${inputFile} > ${inputEncoded}
# ${outputDir}/subword-nmt/apply_bpe.py -c ${codesFile} < ${outputFile} > ${outputEncoded}
