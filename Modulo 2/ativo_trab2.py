### lado ativo (client) ###
import socket
import json

HOST = 'localhost'
PORTA = 5000
ENCODING = "UTF_32"


sock = socket.socket()

sock.connect((HOST,PORTA))

def close_connection():
	print("Finalizando conexão")
	sock.close()

def binary_to_dict(the_binary):
    result = json.loads(the_binary.decode(ENCODING))
    return result
    
print("### CLIENT ###")
while True:
	envio = input("Nome(s) do(s) arquivo(s) separado(s) por espaço: ")
	if (envio=="stop"):
		sock.close()
		break;
	sock.send(envio.encode(ENCODING))
	
	msg=sock.recv(8192)
	
	binary_to_dict(msg)
	print(str(msg,encoding=ENCODING))