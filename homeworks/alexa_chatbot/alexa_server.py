import socket
import json

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
				chatbot_response = "Hi there!"

				connection.sendall(chatbot_response + '\n')

		finally:
			connection.close()
