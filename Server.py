import socket
import threading
import random
import time

max_threads = 5
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server.bind(('172.26.120.100', 9000))
server.bind(('localhost', 9000))
server.listen(5)
print('Aguardando conexões...')

def worker(connection, client_address):
    print(f'Conexão estabelecida com {client_address}')
    connection.settimeout(30)

    expected_seq_number = 0

    while True:
        try:
            data = connection.recv(1024)
        except socket.timeout:
            print(f'Tempo limite excedido. Conexão com {client_address} encerrada.')
            msg = 'TIMEOUT'
            connection.send(msg.encode())
            connection.close()
            break
        except Exception as e:
            print(f'Erro ao receber dados: {e}')
            connection.close()
            break

        print(f'Dados recebidos: {data.decode()}')

        # Adicionar esta linha para verificar se os dados recebidos estão vazios
        if not data:
            print(f'Nenhum dado recebido. Encerrando conexão com {client_address}.')
            connection.close()
            break

        seq_number_received = int(data.decode()[:4])
        checksum_received_str, msg_received = data.decode()[5:].rsplit(' ', 1)
        checksum_received = int(checksum_received_str)
        checksum_calculated = sum([ord(c) for c in msg_received])

        # adiciona a condição de atraso no envio do ack

        start_time = time.time()

        if random.random() < 0.5:  # 50% de chance de atrasar a resposta
            delay = random.uniform(0.5, 3.0)  # tempo de espera aleatório entre 0.5 e 3 segundos
            print(f'Aguardando {delay:.2f} segundos antes de enviar resposta...')
            time.sleep(delay)

        elapsed_time = time.time() - start_time

        if elapsed_time >= 2:
            msg = f'NACK {seq_number_received} ERRO DE TIMEOUT'
            connection.send(msg.encode())
        else:
            if seq_number_received != expected_seq_number:
                msg = f'NACK {seq_number_received} ERRO DE SEQUENCIA'
            elif checksum_received != checksum_calculated:
                msg = f'NACK {seq_number_received} ERRO DE CHECKSUM'
            else:
                msg = f'ACK {seq_number_received}'
                expected_seq_number = (expected_seq_number + 1) % 10000
            connection.send(msg.encode())

        if msg_received.upper() == 'TCHAU':
            connection.close()
            print(f'Conexão com {client_address} encerrada.')
            break

while True:
    try:
        connection, client_address = server.accept()
        print(f'Aguardando cliente {client_address}')

        # verifica se o número máximo de threads foi atingido
        if threading.active_count() < max_threads:
            t = threading.Thread(target=worker, args=(connection, client_address))
            t.start()
        else:
            print(f'Número máximo de threads atingido. Aguardando um pouco...')
            time.sleep(1)
    except Exception as e:
        print(f'Erro ao aceitar conexão: {e}')
        break
