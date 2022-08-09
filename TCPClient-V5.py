"""Tendo por base o programa de acesso a serviços HTTP (em anexo), implemente a capacidade de ler conexão seguras, por meio do encapsulamento de sockets. Além disso, permita também que o usuário especifique uma das opções de linha de comando:
    -p "dados"  -  envio do conjunto de dados na linha de comando por meio de POST
    -f  "nome_arquivo" -  envio do conjunto de dados no arquivo por meio de POST

Assim, a linha de comando seria:

python TCPClient-V5-params.py HOST PORT  RESOURCE -o ARQ_SAIDA  [ -p DADOS | -f ARQ_ENTRADA ]

Se a porta for 443, usar HTTPS, senão usar HTTP.

Aqui os parâmetros -p  e -f são opcionais."""





import socket, sys, ssl, requests, json

SERVER_NAME = sys.argv[1]
PORT = int(sys.argv[2])
CMD = sys.argv[3]



def createSocket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_NAME, PORT))
    return sock

def createSocket_ssl():

    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    sock = context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    sock.connect((SERVER_NAME, 443))
    return sock


def sendHTTPCommand(cmd):
    HTTP_CMD = ("GET "+cmd+" HTTP/1.1\r\n"+
                "Host: "+SERVER_NAME +"\r\n" +
                "\r\n")
    sock.sendall(HTTP_CMD.encode())

def getBodyContentLen(body, lenBody):
    while len(body) < lenBody:
        body += sock.recv(4096)
    return body

def getBodyChunked(response):
    body = b""
    posNL = response.find(b"\r\n")
    lenChunk = int (response[:posNL], 16)
    while lenChunk > 0:
        response = response[posNL+2:]

        while len(response) < lenChunk:
            response += sock.recv(4096)
        body += response[:lenChunk]

        response = response[lenChunk+2:]

        posNL = response.find(b"\r\n")
        while posNL == -1:
            response += sock.recv(4096)
            posNL = response.find(b"\r\n")

        lenChunk = int (response[:posNL], 16)

    return body

def getResponse():
    buffer = sock.recv(4096)

    pos2NL = buffer.find(b"\r\n\r\n")
    headers = buffer[:pos2NL]
    body = buffer[pos2NL+4:]

    print ("Headers:", headers.decode())

    for header in headers.split(b"\r\n"):
        if header.startswith(b"Content-Length:"):
            lenBody = int(header.split(b":")[1])
            body = getBodyContentLen(body, lenBody)
            break
        elif header.startswith(b"Transfer-Encoding:"):
            body = getBodyChunked(body)
            break
    return body

def saveBody(fileName, body):
    fd = open (fileName, "wb")
    fd.write(body)
    fd.close()

def sendHTTPost(sock, SERVER_NAME, CMD, dados):
    HTTP_POST = f"POST {CMD} HTTP/1.1\r\nHost: {SERVER_NAME}\r\nContent-Length: {len(dados)}\r\n\r\n{dados}"
    sock.sendall(HTTP_POST.encode())

if (len(sys.argv) > 8) or (sys.argv[4] != "-o"):
    print ("Uso: ", sys.argv[0], "HOST PORTA SERVICO -o ARQSAIDA | HOST PORTA SERVICO -o ARQSAIDA [-p dados | -f ARQ_ENTRADA]")
    sys.exit(1)


if sys.argv[2] == "443":
    sock = createSocket_ssl()
else:
    sock = createSocket()

if (len(sys.argv) > 8) or (sys.argv[4] != "-o"):
    if sys.argv[6] == '-f':
        with open(sys.argv[7],'r') as arq:
            dados = arq.readlines()
            sendHTTPost(sock, SERVER_NAME, CMD, dados)
    if sys.argv[6] == '-p':
        dados = '?'+sys.argv[7]
        sendHTTPost(sock, SERVER_NAME, CMD, dados)


sendHTTPCommand(CMD)
body = getResponse()
sock.close()
saveBody(sys.argv[5], body)
