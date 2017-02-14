import socket
import json


def talk_to_server(user_utterance):
	reply = ""

	with open('config.json') as config_file:
		data = json.load(config_file)
		serv_addr = data["server_address"]
		port = data["port"]

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = (serv_addr, port)
	sock.connect(server_address)

	try:
		sock.sendall(user_utterance + '\n')

		print("HERE")

		while "\n" not in reply:
			data = sock.recv(16)
			if len(data) <= 0:
				print("something went wrong")
				break

			print("here with " + str(data))

			reply += data
	except:
		print("problem communicating with server")

	return reply
			
