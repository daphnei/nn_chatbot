import socket
import sys

if __name__ == "__main__":
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	server_address = ('lvn403-6.grasp.upenn.edu', 62219)
	print('starting up on %s port %s' % server_address)
	sock.bind(server_address)

	sock.listen(1)

	amount_expected = 150

	user_utterance = ""

	while True:
		print('waiting for a connection')
		connection, client_address = sock.accept()
		print('connection from', client_address)

		try:
			
			while "\n" not in user_utterance and len(user_utterance) <= amount_expected:
				print("in while")
				data = connection.recv(16)
				user_utterance += data

			if data:
				print("User: " + user_utterance)
			else:
				print("no more data from ", client_address)
				break

			connection.sendall("Hi there!\n")
		finally:
			connection.close()