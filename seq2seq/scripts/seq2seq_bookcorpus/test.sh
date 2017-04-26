predDir="books/pred"
modelDir="books/model"
devSources="books/test.txt"

cd ..

mkdir -p ${predDir}

python3 -m bin.infer \
  --tasks "
    - class: DecodeText" \
  --model_dir ${modelDir} \
  --input_pipeline "
    class: ParallelTextInputPipeline
    params:
      source_files:
        - ${devSources}" \
 >>  ${predDir}/predictions.txt
