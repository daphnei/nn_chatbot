import socket
import json
import tensorflow as tf
import sys

sys.path.append('../seq2seq/')
import translate

if __name__ == "__main__":
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	with open('config.json') as config_file:
		data = json.load(config_file)
		serv_addr = data["server_address"]
		port = data["port"]

	server_address = (serv_addr, port)

	print('starting up on %s port %s' % server_address)
	sock.bind(server_address)

	sock.listen(1)

	amount_expected = 150

	FLAGS = tf.app.flags.FLAGS
	FLAGS.data_dir = data["tf_data_dir"]
	FLAGS.train_dir = data["tf_checkpoints"]

 	with tf.Session() as sess:
 		# Create model and load parameters.
		(model, in_vocab, out_vocab) = translate.init_decode(sess)
		
		while True:
			user_utterance = ""
			print('waiting for a connection')
			connection, client_address = sock.accept()
			print('connection from', client_address)

			try:
				
				while "\n" not in user_utterance:
					print("in while")
					data = connection.recv(16)
					if len(data) <= 0:
						print("something went wrong")
						break
					user_utterance += data

				if user_utterance:
					stripped_utterance = user_utterance.rstrip()

					print("User: " + user_utterance + " ||| " + stripped_utterance)

					chatbot_response = str(translate.decode_sentence(sess, model, in_vocab, out_vocab, stripped_utterance))

					connection.sendall(chatbot_response + '\n')

			finally:
				connection.close()
