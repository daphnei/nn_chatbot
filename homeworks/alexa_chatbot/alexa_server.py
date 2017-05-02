import socket
import json
import tensorflow as tf
import sys

CONV_START = "0"
CONV_CONT = "1"
CONV_ACCEPT = "2"
CONV_REJECT = "3"
CONV_END = "4"


sys.path.append('../seq2seq/')
import translate

storyTurns = []

class Turn(object):
	def __init__(self, query, response, accepted):
		self.query = query
		self.response = response
		self.accepted = accepted


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
	#
	# FLAGS = tf.app.flags.FLAGS
	# FLAGS.data_dir = data["tf_data_dir"]
	# FLAGS.train_dir = data["tf_checkpoints"]

 	# with tf.Session() as sess:
 		# Create model and load parameters.
		# (model, in_vocab, out_vocab) = translate.init_decode(sess)

	lastTurn = Turn("", "", False)

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
				chatbot_response = "something bad happened"

				queryCommand = stripped_utterance[0]

				if queryCommand == CONV_START:
					#chatbot_response = str(translate.decode_sentence(sess, model, in_vocab, out_vocab, stripped_utterance))
					chatbot_response = "hellllloo"
					lastTurn.query = stripped_utterance[1:]
					lastTurn.response = chatbot_response

				if queryCommand == CONV_ACCEPT:
					chatbot_response = "" + CONV_CONT
					lastTurn.accepted = True
				if queryCommand == CONV_REJECT:
					chatbot_response = "" + CONV_CONT
					lastTurn.accepted = False

				if queryCommand == CONV_END:
					chatbot_response = ""

					for t in storyTurns:
						if t.accepted:
							chatbot_response += (" " + t.query + " " + t.response);


				if queryCommand == CONV_ACCEPT or queryCommand == CONV_REJECT:
					storyTurns.append(lastTurn)


				connection.sendall(chatbot_response + '\n')
				print(chatbot_response)

		finally:
			connection.close()
