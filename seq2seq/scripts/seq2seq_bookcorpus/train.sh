#!/bin/sh

DATA_PATH="/media/snake/daphne/school/nn_chatbot/seq2seq/scripts/train_processed"
SEQ2SEQ_PATH="/media/snake/daphne/school/nn_chatbot/seq2seq"
# SEQ2SEQ_PATH="."

export PYTHONPATH=$SEQ2SEQ_PATH

VOCAB_SOURCE=${DATA_PATH}/vocab.tok.txt
VOCAB_TARGET=${DATA_PATH}/vocab.tok.txt

TRAIN_SOURCES=${DATA_PATH}/input_short.txt
TRAIN_TARGETS=${DATA_PATH}/output_short.txt

TRAIN_STEPS=1000000

MODEL_DIR="$SEQ2SEQ_PATH/model/book1"

mkdir -p $MODEL_DIR

     # $SEQ2SEQ_PATH/example_configs/train_seq2seq.yml,
     # $SEQ2SEQ_PATH/example_configs/text_metrics_bpe.yml" \
python "$SEQ2SEQ_PATH/bin/train.py"  \
  --config_paths="$DATA_PATH/model.yaml" \
  --model_params "
      vocab_source: $VOCAB_SOURCE
      vocab_target: $VOCAB_TARGET" \
  --input_pipeline_train "
    class: ParallelTextInputPipeline
    params:
      source_files:
        - $TRAIN_SOURCES
      target_files:
        - $TRAIN_TARGETS" \
  --input_pipeline_dev "
    class: ParallelTextInputPipeline
    params:
       source_files:
        - $TRAIN_SOURCES
       target_files:
        - $TRAIN_TARGETS" \
  --batch_size 32 \
  --train_steps $TRAIN_STEPS \
  --output_dir $MODEL_DIR \
  --gpu_allow_growth \
  --gpu_memory_fraction 0.2

