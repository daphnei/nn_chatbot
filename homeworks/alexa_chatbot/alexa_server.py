import socket
import json
import tensorflow as tf
import sys
from infer_on_one import SingleInference

CONV_START = "0"
CONV_CONT = "1"
CONV_ACCEPT = "2"
CONV_REJECT = "3"
CONV_END = "4"

sys.path.append('../seq2seq/')

storyTurns = []

class Turn(object):
	def __init__(self, query, response, accepted):
		self.query = query
		self.response = response
		self.accepted = accepted
		self.invalid = True


if __name__ == "__main__":
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	MODEL_DIR = "/chatdata/models/books_100k"
	VOCAB_PATH = "/chatdata/vocab.tok.txt"

	# current prediction time ~20ms
	sl = SingleInference(MODEL_DIR, VOCAB_PATH)

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

	chatbot_response = sl.query_once("test")
	print(chatbot_response) 

	last_turn = Turn("", "", False)

	while True:
		user_utterance = ""
		print('waiting for a connection')
		connection, client_address = sock.accept()
		print('connection from', client_address)

		try:
			while "\n" not in user_utterance:
				data = connection.recv(16)
				if len(data) <= 0:
					print("something went wrong")
					break
				user_utterance += data
			if user_utterance:
				stripped_utterance = user_utterance.rstrip()

				print("User says: " + stripped_utterance)

				queryCommand = stripped_utterance[0]

				chatbot_response = ""
				if queryCommand == CONV_START:
					last_turn.query = stripped_utterance[1:]
					chatbot_response = sl.query_once(last_turn.query) 
					last_turn.response = chatbot_response
					last_turn.invalid = False

				elif queryCommand == CONV_ACCEPT:
					chatbot_response = "" + CONV_CONT
					last_turn.accepted = True
				elif queryCommand == CONV_REJECT:
					chatbot_response = "" + CONV_CONT
					last_turn.accepted = False
				elif queryCommand == CONV_END:
					chatbot_response = ""

					for t in storyTurns:
						if t.accepted:
							chatbot_response += (" " + t.query + ". " + t.response + ".")

					storyTurns = []
				else:
					print("Got an unknown command from the server: " + queryCommand)


				if queryCommand == CONV_ACCEPT or queryCommand == CONV_REJECT:
					if not last_turn.invalid:
						storyTurns.append(last_turn)
						last_turn = Turn("", "", False)


				connection.sendall(chatbot_response + '\n')
				print("Alexa response with: " + chatbot_response)

		finally:
			connection.close()
