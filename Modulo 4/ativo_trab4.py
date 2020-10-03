### lado ativo (client) ###
### BATE PAPO DISTRIBUÍDO ###
import json
import socket
import sys
import threading

HOST = 'localhost'
PORTA = 5002
ENCODING = "UTF-8"

isOnChat = False
receiverID = -1
isActive = True

sock = socket.socket()
sock.connect((HOST, PORTA))


def CloseConnection():
    print("Finalizando conexão")
    sock.close()
    sys.exit()


# Converte de Binário para Dicionário
def BinaryToDict(the_binary):
    result = json.loads(the_binary.decode(ENCODING))
    return result


def QuickSend(socket, message):
    socket.send(message.encode(ENCODING))


def QuickReceive(socket, size):
    msgRecv = socket.recv(size)
    msgStr = str(msgRecv, encoding=ENCODING)
    return msgStr


def QuickReceiveAndPrint(socket, size):
    msgStr = QuickReceive(socket, size)
    print("\n" + msgStr)
    return msgStr


def CommandList():
    print("Para ter acesso à lista de comandos, digite \"--help\":")
    print("--listar : Lista as conexões disponíveis para chat")
    print("--trocar : Troca o atual destinatário")
    print("--stop : Encerra o cliente")


# Separa a mensagem recebida do ID de quem enviou
def separateMsg(msgStr):
    idStart = msgStr.index('[[')
    idEnd = msgStr.index(']]')
    senderId = msgStr[idStart + 2:idEnd]
    msgContent = msgStr[idEnd + 2:]

    return senderId, msgContent


# Envia e recebe mensagem com prefixo do destinatário
def HandleP2PMessage(clientSocket, messageToChat):
    global isOnChat, receiverID
    messagePrefix = "[[" + str(receiverID) + "]]"
    QuickSend(clientSocket, messagePrefix + messageToChat)
    thereIs = QuickReceive(clientSocket, 512)  # Verifica se há mensagens na fila
    if thereIs:
        senderID, msgContent = separateMsg(thereIs)
        print("Mensagem de {%s}: %s" % (senderID, msgContent))

    if thereIs == "notOk":
        QuickReceiveAndPrint(clientSocket, 1024)

    while thereIs == "yes":  # Enquanto houver mensagens na fila, recebe do server
        QuickReceiveAndPrint(clientSocket, 8192)
        thereIs = QuickReceive(clientSocket, 512)


# Envia e recebe mensagem com prefixo do destinatário
def HandleP2PMessage2(clientSocket, messageToChat):
    global isOnChat, receiverID
    try:
        messagePrefix = "[[" + str(receiverID) + "]]"
        QuickSend(clientSocket, messagePrefix + messageToChat)
    except:
        print("Não conseguimos enviar a mensagem: %s" % (messageToChat))


# Verifica se o cliente digitou algum comando
def ChooseAction(inputFromClient):
    global isActive
    listToIgnore = [" ", "\\n", ""]

    if inputFromClient in listToIgnore:
        print("Nada foi digitado")

    elif inputFromClient == "--stop":
        isActive = False
        CloseConnection()

    elif inputFromClient == "--help":
        CommandList()

    elif inputFromClient == "--listar":
        QuickSend(sock, inputFromClient)
        QuickReceiveAndPrint(sock, 8192)

    elif inputFromClient == "--trocar":
        QuickSend(sock, inputFromClient)
        QuickReceiveAndPrint(sock, 8192)
        changeTo = input("Digite o número referente a conexão que você deseja conversar: ")
        QuickSend(sock, changeTo)
        okMsg = QuickReceive(sock, 1024)
        if okMsg == "ok":
            global receiverID
            receiverID = changeTo
            global isOnChat
            isOnChat = True
            print("OK\n")
        else:
            print(okMsg)


print("### CLIENT ###")
CommandList()


# def main():

def receiveMsgs(clientSocket):
    global isActive
    while isActive:
        msg = QuickReceive(clientSocket, 1024)
        if msg:
            senderID, msgContent = separateMsg(msg)
            print("Mensagem de {%s}: %s" % (senderID, msgContent))
    return


def readInputAndSend(clientSocket):
    global isActive
    while isActive:
        if receiverID == -1:
            toSend = input("Conversando com {Ninguém}, escolha alguém com \"--trocar\" \n ")
        else:
            toSend = input("Conversando com {%s}: " % receiverID)

        if toSend.find('--') == 0:
            ChooseAction(toSend)
        else:
            HandleP2PMessage2(clientSocket, toSend)
    return

def main():
    receive = threading.Thread(target=receiveMsgs, args=sock)
    send = threading.Thread(target=readInputAndSend, args=sock)

    while isActive:
        continue
    print("Encerrando cliente.")
    receive.join()
    send.join()
    sock.close()
    sys.exit()


main()

# while True:
#     if receiverID == -1:
#         toSend = input("Conversando com {Ninguém}, escolha alguém com \"--trocar\" \n ")
#     else:
#         toSend = input("Conversando com {%s}: " % receiverID)
#         HandleP2PMessage(sock, toSend)
#     ChooseAction(toSend)
#
#     # msgRecv = sock.recv(8192)
#     # print(str(msgRecv, encoding=ENCODING))
#
#     '''resultDicts = BinaryToDict(msg)
#
#     for eachDictionary in resultDicts:
#         print("\"" + eachDictionary + "\": " + str(resultDicts[eachDictionary]))'''

# main()
