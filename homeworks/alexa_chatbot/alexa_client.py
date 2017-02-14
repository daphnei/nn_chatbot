import socket
import sys


def talk_to_server(user_utterance):
	reply = ""

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = ('lvn403-6.grasp.upenn.edu', 62219)
	sock.connect(server_address)

	try:
		sock.sendall(user_utterance)

		amount_expected = 150
		print("HERE")

		while "\n" not in reply and len(reply) <= amount_expected:
			data = sock.recv(16)
			print("here with " + str(data))

			reply += data
	except:
		print("problem communicating with server")

	return reply
			