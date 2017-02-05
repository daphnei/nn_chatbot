import numpy as np
import tensorflow as tf
import random
import time

QUIET = False
WRITE_TO_TENSORBOARD = False

def get_batch(batch_size):
	options = [([0,1], [1, 0]), ([0,0], [1, 0]), ([1, 1], [0, 1]), ([1,0], [1, 0])]

	x = np.zeros([batch_size, 2], dtype='float')
	y = np.zeros([batch_size, 2], dtype='float')

	# This code fills in batches randomly, which doesn't work consistently for small
	# batches, but seems more 'real world' to me.
	for i in xrange(0, batch_size):
		chosen = random.choice(options)
		x[i,:] = np.array(chosen[0], dtype='float').reshape([1,2])
		y[i,:] = np.array(chosen[1], dtype='float').reshape([1,2])
	return (x, y) 

	# This code makes sure each batch has about the same number of each example.
	# for i in xrange(0, batch_size):
		# chosen = options[i%4]
		# x[i,:] = np.array(chosen[0], dtype='float').reshape([1,2])
		# y[i,:] = np.array(chosen[1], dtype='float').reshape([1,2])
	# return (x, y) 
 
def variable_summaries(var):
	"""Attach a lot of summaries to a Tensor (for TensorBoard visualization)."""
	with tf.name_scope('summary'):
		mean = tf.reduce_mean(var)
		tf.summary.scalar('mean', mean)
		with tf.name_scope('stddev'):
			stddev = tf.sqrt(tf.reduce_mean(tf.square(var - mean)))
		tf.summary.scalar('stddev', stddev)
		tf.summary.scalar('max', tf.reduce_max(var))
		tf.summary.scalar('min', tf.reduce_min(var))
		tf.summary.histogram('histogram', var)

def add_fully_connected(x, input_dim, output_dim):
	with tf.name_scope('fc'):
		with tf.name_scope('weights'):
			weights = tf.Variable(tf.truncated_normal([input_dim, output_dim], mean=0, stddev=1/np.sqrt(input_dim)), name='weights');
			variable_summaries(weights)
		with tf.name_scope('biases'):
			biases = tf.Variable(tf.zeros([output_dim]), name='biases')
			variable_summaries(biases)
	return tf.matmul(x, weights) + biases

def run_network(batch_size, num_steps, num_hidden, num_hidden_layers, learning_rate, adam = True, activation='relu'):	
	with tf.Graph().as_default():
		# with tf.device('/gpu:2'):
		# Define variables.
		x = tf.placeholder(tf.float32, [batch_size, 2], name='x')
		y = tf.placeholder(tf.float32, [batch_size, 2], name='y') 

		last_layer = x	
		last_layer_dim = 2

		activ_func = tf.nn.relu
		if activation == 'sigmoid':
			activ_func = tf.nn.sigmoid
		elif activation == 'tanh':
			activ_func = tf.nn.tanh
	
		# Add specified number of hidden layers.
		for i in xrange(0, num_hidden_layers):
			print 'Adding hidden layer with %d nodes' % (num_hidden)
			hidden = activ_func(add_fully_connected(last_layer, last_layer_dim, num_hidden))
			last_layer = hidden
			last_layer_dim = num_hidden

		output = add_fully_connected(last_layer, last_layer_dim, 2)

		loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits = output, labels = y), name='loss')

		tf.summary.scalar('loss', loss)


		if adam:
			optimizer = tf.train.AdamOptimizer(learning_rate)
		else:
			optimizer = tf.train.GradientDescentOptimizer(learning_rate)

		global_step = tf.Variable(0, name='global_step', trainable=False)
		optim = optimizer.minimize(loss, global_step=global_step)

		summary = tf.summary.merge_all()

		with tf.Session() as sess:
			summary_writer = tf.summary.FileWriter("train_dir", sess.graph)
			
			init = tf.global_variables_initializer()
			sess.run(init)	

			for step in xrange(1, num_steps):
				data_x, data_y = get_batch(batch_size)
				feed_dict = {x: data_x, y: data_y}

				start_time = time.time()
				_, loss_value, summary_str = sess.run([optim, loss, summary],
                             feed_dict=feed_dict)
				duration = time.time() - start_time
				
				if step % 10 == 0 and WRITE_TO_TENSORBOARD:	
					summary_writer.add_summary(summary_str, step)

				if step % 50 == 0:
					# print data_x
					num_correct_op = tf.equal(tf.argmax(data_y, 1), tf.argmax(output, 1))
					accuracy = np.sum(sess.run(num_correct_op, feed_dict=feed_dict)) / float(batch_size)

					# check the results on 100*batch_size 'test' examples
					num_correct = 0
					for i in xrange(0, 10):
						data = get_batch(batch_size)
						f_dict = {x: data[0], y: data[1]}	
						out = sess.run(output, f_dict)
					
						num_correct_op = tf.equal(tf.argmax(data_y, 1), tf.argmax(output, 1))
						num_correct = num_correct + np.sum(sess.run(num_correct_op, feed_dict=feed_dict))
					test_accuracy = num_correct / float(10 * batch_size)

					if not QUIET:
						print 'Step %d: loss = %.2f, batch acc = %.2f, test acc = %.2f (%.3f sec)' % (step, loss_value, accuracy, test_accuracy, duration)	

					if accuracy == 1.0:
						# Good enough exit
						print 'Test accuracy is perfect after %d iterations. Quitting.' % (step)
						return
			print 'After %d iterations, the network has still not converged. Something must be very wrong.' % (num_steps)

if __name__ == "__main__":
	batch_size = 100
	num_steps = 100
	num_hidden = 7
	num_hidden_layers = 2
	learning_rate = 0.2

	run_network(batch_size, num_steps, num_hidden, num_hidden_layers, learning_rate, False, 'relu')
