# TCP-Client-v5

Tendo por base o programa de acesso a serviços HTTP (em anexo), implemente a capacidade de ler conexão seguras, por meio do encapsulamento de sockets. Além disso, permita também que o usuário especifique uma das opções de linha de comando:
    -p "dados"  -  envio do conjunto de dados na linha de comando por meio de POST
    -f  "nome_arquivo" -  envio do conjunto de dados no arquivo por meio de POST

Assim, a linha de comando seria:

python TCPClient-V5-params.py HOST PORT  RESOURCE -o ARQ_SAIDA  [ -p DADOS | -f ARQ_ENTRADA ]

Se a porta for 443, usar HTTPS, senão usar HTTP.

Aqui os parâmetros -p  e -f são opcionais.
