from pydoc import locate
import tensorflow as tf
import numpy as np
from seq2seq import tasks, models
from seq2seq.training import utils as training_utils
from seq2seq.tasks.inference_task import InferenceTask, unbatch_dict


class DecodeOnce(InferenceTask):
  '''
  Similar to tasks.DecodeText, but for one input only.
  Source fed via features.source_tokens and features.source_len
  '''
  def __init__(self, params, callback_func):
    super(DecodeOnce, self).__init__(params)
    self.callback_func=callback_func
  
  @staticmethod
  def default_params():
    return {}

  def before_run(self, _run_context):
    fetches = {}
    fetches["predicted_tokens"] = self._predictions["predicted_tokens"]
    fetches["features.source_tokens"] = self._predictions["features.source_tokens"]
    return tf.train.SessionRunArgs(fetches)

  def after_run(self, _run_context, run_values):
    fetches_batch = run_values.results
    for fetches in unbatch_dict(fetches_batch):
      # Convert to unicode
      fetches["predicted_tokens"] = np.char.decode(
          fetches["predicted_tokens"].astype("S"), "utf-8")
      predicted_tokens = fetches["predicted_tokens"]

      # If we're using beam search we take the first beam
      # TODO: beam search top k
      if np.ndim(predicted_tokens) > 1:
        predicted_tokens = predicted_tokens[:, 0]

      fetches["features.source_tokens"] = np.char.decode(
          fetches["features.source_tokens"].astype("S"), "utf-8")
      source_tokens = fetches["features.source_tokens"]
      
      self.callback_func(source_tokens, predicted_tokens)

class SingleInference:
  def __init__(self, model_dir, vocab_path):
    checkpoint_path = tf.train.latest_checkpoint(model_dir)
  
    # Load saved training options
    train_options = training_utils.TrainOptions.load(model_dir)

    # Create the model
    model_cls = locate(train_options.model_class) or \
      getattr(models, train_options.model_class)
    model_params = train_options.model_params

    model = model_cls(
        params=model_params,
        mode=tf.contrib.learn.ModeKeys.INFER)

    # first dim is batch size
    self.source_tokens_ph = tf.placeholder(dtype=tf.string, shape=(1, None))
    self.source_len_ph = tf.placeholder(dtype=tf.int32, shape=(1,))

    model(
      features={
        "source_tokens": self.source_tokens_ph,
        "source_len": self.source_len_ph
      },
      labels=None,
      params={
        "vocab_source": vocab_path,
        "vocab_target": vocab_path
      }
    )

    saver = tf.train.Saver()
 
    def _session_init_op(_scaffold, sess):
      saver.restore(sess, checkpoint_path)
      tf.logging.info("Restored model from %s", checkpoint_path)

    scaffold = tf.train.Scaffold(init_fn=_session_init_op)
    session_creator = tf.train.ChiefSessionCreator(scaffold=scaffold)

    # A hacky way to retrieve prediction result from the task hook...
    self.prediction_dict = {}

    def _save_prediction_to_dict(source_tokens, predicted_tokens):
      self.prediction_dict[self._tokens_to_str(source_tokens)] = self._tokens_to_str(predicted_tokens)

    self.sess = tf.train.MonitoredSession(
      session_creator=session_creator,
      hooks=[DecodeOnce({}, callback_func=_save_prediction_to_dict)])
 
  def query_once(self, source_tokens):
    tf.reset_default_graph()
    source_tokens = source_tokens.split() + ["SEQUENCE_END"]
    self.sess.run([], {
        self.source_tokens_ph: [source_tokens],
        self.source_len_ph: [len(source_tokens)]
      })
    return self.prediction_dict.pop(self._tokens_to_str(source_tokens))

  def _tokens_to_str(self, tokens):
    return " ".join(tokens).split("SEQUENCE_END")[0].strip()

if __name__ == "__main__":
  MODEL_DIR = "/chatdata/models/books_100k"
  VOCAB_PATH = "/chatdata/vocab.tok.txt"

  # current prediction time ~20ms
  si = SingleInference(MODEL_DIR, VOCAB_PATH)

  samples = [
    u"once upon a time, there was a princess",
    u"do you want to go horseback riding with me",
    u"she said"
  ]
  for sample_in in samples:
    print(sample_in)
    print(si.query_once(sample_in))
    print()
  
