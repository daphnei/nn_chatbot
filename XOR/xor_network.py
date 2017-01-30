import numpy as np
import tensorflow as tf
import random
import time

def get_batch():
	options = [([0,1], [1, 0]), ([0,0], [0, 1]), ([1, 1], [0, 1]), ([1,0], [1, 0])]
	chosen = random.choice(options)

	x = np.array(chosen[0], dtype='float').reshape([1,2])
	y = np.array(chosen[1], dtype='float').reshape([1,2])
	return (x, y) 

def variable_summaries(variables):
	"""Attach a lot of summaries to a Tensor (for TensorBoard visualization)."""
	for var in variables:
		with tf.name_scope('summaries'):
			mean = tf.reduce_mean(var)
			stddev = tf.sqrt(tf.reduce_mean(tf.square(var - mean)))
			
			tf.summary.scalar('mean', mean)
			tf.summary.scalar('stddev', stddev)
			tf.summary.scalar('max', tf.reduce_max(var))
			tf.summary.scalar('min', tf.reduce_min(var))
			tf.summary.histogram('histogram', var)
	 
if __name__ == '__main__':
	with tf.Graph().as_default():
		# Define variables.
		x = tf.placeholder(tf.float32, [1, 2], name='x')
		y = tf.placeholder(tf.float32, [1, 2], name='y') 

		with tf.name_scope('hidden0'):
			weights0 = tf.Variable(tf.truncated_normal([2, 10], mean=0, stddev=0.01), name='weights');
			biases0 = tf.Variable(tf.zeros([10]), name='biases')
	
		with tf.name_scope('hidden1'):
			weights1 = tf.Variable(tf.truncated_normal([10, 10], mean=0, stddev=0.01), name='weights');
			biases1 = tf.Variable(tf.zeros([10]), name='biases')
		
		with tf.name_scope("output"):
			weights2 = tf.Variable(tf.truncated_normal([10, 2], mean=0, stddev=0.01), name='weights');
			biases2 = tf.Variable(tf.zeros([2]), name='biases')

		# variable_summaries([weights0, biases0, weights1, biases1, weights2, biases2])

		#hidden1 = tf.nn.relu(tf.matmul(x, tf.get_variable('hidden1/weights')) + tf.get_variable('hidden1/biases'))
		#hidden2 = tf.nn.relu(tf.matmul(hidden1, tf.get_variable('hidden2/weights')) + tf.get_variable('hidden2/biases'))
		hidden0 = tf.nn.relu(tf.matmul(x, weights0) + biases0)
		hidden1 = tf.nn.relu(tf.matmul(hidden0, weights1) + biases1)
		output = (tf.matmul(hidden1, weights2) + biases2)

		loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(output, y), name='loss')

		# Generates a snapshot of the loss function every time a summary is written out
		tf.scalar_summary('loss', loss)

		learning_rate = 0.01

		# optimizer = tf.train.AdamOptimizer(learning_rate)
		optimizer = tf.train.GradientDescentOptimizer(learning_rate)

		global_step = tf.Variable(0, name='global_step', trainable=False)
		optim = optimizer.minimize(loss, global_step=global_step)

		summary = tf.summary.merge_all()

		with tf.Session() as sess:
			summary_writer = tf.summary.FileWriter("train_dir", sess.graph)
			
			init = tf.global_variables_initializer()
			sess.run(init)	

			for step in xrange(1, 3000):
				data_x, data_y = get_batch()
				feed_dict = {x: data_x, y: data_y}

				start_time = time.time()
				_, loss_value, summary_str = sess.run([optim, loss, summary],
                             feed_dict=feed_dict)
				duration = time.time() - start_time
				
				if step % 10 == 0:	
					summary_writer.add_summary(summary_str, step)

				if step % 100 == 0:
					print data_x
					print 'Step %d: loss = %.2f (%.3f sec)' % (step, loss_value, duration)	

			# check the results on some examples
			for i in xrange(0,10):
				data = get_batch()
				f_dict = {x: data[0], y: data[1]}	
				print f_dict
				out = sess.run(output, f_dict)
				print out[0, 0] > out[0, 1]
				print out
				print "\n"
