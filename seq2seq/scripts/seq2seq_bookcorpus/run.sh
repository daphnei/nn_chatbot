#!/bin/sh

DATA_PATH="/data"
MODEL_PATH="/data/models/books_v1"
PREDICTIONS_PATH="$MODEL_PATH/predictions"

SEQ2SEQ_PATH="../.."
CONFIG_PATH="."

export PYTHONPATH=$SEQ2SEQ_PATH

VOCAB_SOURCE=${DATA_PATH}/vocab.tok.txt
VOCAB_TARGET=${DATA_PATH}/vocab.tok.txt

TRAIN_SOURCES=${DATA_PATH}/train_input.txt
TRAIN_TARGETS=${DATA_PATH}/train_output.txt

DEV_SOURCES=${DATA_PATH}/dev_input.txt
DEV_TARGETS=${DATA_PATH}/dev_output.txt

TRAIN_STEPS=1000000

mkdir -p $MODEL_PATH

op=$1


    #--config_paths="$CONFIG_PATH/text_metrics.yml, $CONFIG_PATH/model.yaml, " \

if [ "$op" = "train" ]; then
     # $SEQ2SEQ_PATH/example_configs/train_seq2seq.yml,
     # $SEQ2SEQ_PATH/example_configs/text_metrics_bpe.yml" \
  python "$SEQ2SEQ_PATH/bin/train.py"  \
    --config_paths="$CONFIG_PATH/model_v1.yaml" \
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
    --batch_size 32 \
    --train_steps $TRAIN_STEPS \
    --output_dir $MODEL_PATH \
    --gpu_allow_growth \
    --gpu_memory_fraction 0.8 \
    --buckets 20,40

elif [ "$op" = "test" ]; then
python -m bin.infer \
  --tasks "
    - class: DecodeText
    - class: DumpBeams
      params:
        file: ${PREDICTIONS_PATH}/beams.npz" \
  --model_dir $MODEL_PATH \
  --model_params "
    inference.beam_search.beam_width: 5" \
  --input_pipeline "
    class: ParallelTextInputPipeline
    params:
      source_files:
        - $DEV_SOURCES" \
  > ${PREDICTIONS_PATH}/predictions.txt
#else
#  echo "Operation not supported."
fi
