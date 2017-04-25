#~/bin/sh

export DATA_PATH=/media/snake/daphne/school/nn_chatbot/book_corpus_tagged/processed_fancy

export VOCAB_SOURCE=${DATA_PATH}/vocab.bpe.32000
export VOCAB_TARGET=${DATA_PATH}/vocab.bpe.32000
export TRAIN_SOURCES=${DATA_PATH}/train.tok.bpe.32000
export TRAIN_TARGETS=${DATA_PATH}/train.tok.bpe.32000
export DEV_SOURCES=${DATA_PATH}/test.tok.bpe.32000
export DEV_TARGETS=${DATA_PATH}/test.tok.bpe.32000

export DEV_TARGETS_REF=${DATA_PATH}/test.tok
export TRAIN_STEPS=1000000

MODEL_DIR=/media/snake/daphne/school/nn_chatbot/tr_data/models
TRAIN_STEPS=None
python -m bin.train \
  --config_paths="run.yaml" \
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
        - $DEV_SOURCES
       target_files:
        - $DEV_TARGETS" \
  --batch_size 4  \
  --output_dir $MODEL_DIR
