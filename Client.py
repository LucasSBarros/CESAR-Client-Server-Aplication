import socket
import random
import time

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.settimeout(10)  # tempo limite de 10 segundos
#cliente.connect(('172.26.120.100', 9000))
cliente.connect(('localhost', 9000))

seq_number = 0

while True:
    mensagem_batch = input('Escreva as mensagens separadas por "||": ')
    if mensagem_batch.upper() == 'TCHAU':
        cliente.close()
        exit()

    messages = mensagem_batch.split('||')
    for mensagem in messages:
        seq_number_str = f'{seq_number:04d}'
        checksum = sum([ord(c) for c in mensagem])
        mensagem_with_seq = f'{seq_number_str} {checksum} {mensagem}'
        lost_package1 = f'{seq_number_str} {checksum} {""}'
        lost_package2 = f'{"9999"} {checksum} {mensagem}'

        while True:
            # adiciona a condição de perda de pacotes
            package_loss = random.random()
            if package_loss < 0.5:  # 50% de chance de enviar a mensagem
                cliente.send(mensagem_with_seq.encode())
            elif package_loss >= 0.5 and package_loss < 0.75:
                print("Simulando perda de pacote por checksum ...")
                time.sleep(1)  # simula um atraso na transmissão
                cliente.send(lost_package1.encode())
            else:
                print("Simulando perda sequencial de pacotes...")
                time.sleep(1)  # simula um atraso na transmissão
                cliente.send(lost_package2.encode())

            try:
                resposta = cliente.recv(1024)
            except socket.timeout:
                print("Tempo limite excedido. Encerrando conexão...")
                cliente.close()
                exit()
            print(f'Resposta do servidor: {resposta.decode()}')

            if resposta.decode()[:3] == 'ACK':
                seq_number = (seq_number + 1) % 10000
                break
            elif resposta.decode()[:4] == 'NACK':
                print(f'Reenviando mensagem original: {mensagem_with_seq}')
