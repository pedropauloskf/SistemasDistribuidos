import socket, select, sys, threading

HOST = 'localhost'
ENTRADAS = [sys.stdin]  # define entrada padrão

x = 0
myId = -1
primaryCopy = False           #Variavel que diz quem esta com o chapeu para poder alterar X
changesHistory = {}
connectionsList = {1: 5001, 2: 5002, 3: 5003, 4: 5004}

# Inicia o servidor e adiciona o socket do servidor nas entradas
def StartServer(myId):
    global HOST, connectionsList
    global ENTRADAS
    print("myId: %s, my port %i" %(myId, connectionsList[myId] ))

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = int(connectionsList[myId])
    sock.bind((HOST, port ))
    sock.listen(5)  # espera por até 5 conexões
    sock.setblocking(False)  # torna o socket não bloqueante na espera por conexões
    ENTRADAS.append(sock)
    return sock

def SetPrimaryCopy():
    global primaryCopy
    primaryCopy = True

# gerencia o recebimento de conexões de clientes, recebe o sock do server
def NewClient(sock):
    newSocket, endereco = sock.accept()
    print('Conectado com: ' + str(endereco))

    '''CONEXOES[endereco] = newSocket  # registra a nova conexão no dicionário de conexões
    if len(ID_ENDERECO) == 0:
        ID_ENDERECO[1] = endereco
    else:
        index = max(ID_ENDERECO, key=ID_ENDERECO.get) + 1
        ID_ENDERECO[index] = endereco'''
    

    return newSocket, endereco

def PrintCommandList():
    print("--help - lista os comandos")
    print("--valor - valor de x nesta réplica")
    print("--historico - historico do valor de x")
    print("--alterar - altera o valor de x")
    print("--fim - finaliza esta replica")

def Processing(command, mySock):
    if command == "--help":
        PrintCommandList()
    if command == "--valor":
        global x
        print(x)
    if command == "--historico":
        global changesHistory
        print(changesHistory)
    if command == "--alterar":
        Altera_X(mySock)
    if command == "--fim":
        exit()

def Altera_X(mySock):
    global myId
    mySock.connect((HOST, 5004 ))
    '''for i in connectionsList:
        if i != myId:
            print("Connecting to id %s, port %i" %(i, connectionsList[i]))
            mySock.connect((HOST, connectionsList[i]))
'''
def main():
    global myId

    for ids in range(1,5):
        newReplicaThread = threading.Thread(target=StartServer, args=(ids,) )
        newReplicaThread.start()

    while myId not in range(1,5):
        myId = int(input("\nDigite o numero desta réplica: \n"))

    #mySock = StartServer(myId)

    PrintCommandList()

    #while True:
    #    command = input("Digite o comando: ")
    #    Processing(command, mySock)


    #print("### %s - ESPERANDO POR CONEXÕES ###" %(myId))

    while True:
        leitura, escrita, excecao = select.select(ENTRADAS, [], [])  # listas do select

        # percorre cada objeto de leitura (conexão socket, entrada de teclado)
        for leitura_input in leitura:
            # significa que a leitura recebeu pedido de conexão
            if leitura_input == mySock:
                clientSock, endr = NewClient(mySock)

                # cria e inicia nova thread para atender o cliente
                #newClientThread = threading.Thread(target=Processing, args=(clientSock, endr))
                #newClientThread.start()
                
            elif leitura_input == sys.stdin:  # entrada padrão, teclado
                #cmd = input()
                command = input("Digite o comando: ")
                Processing(command, mySock)

if __name__ == "__main__":
    main()