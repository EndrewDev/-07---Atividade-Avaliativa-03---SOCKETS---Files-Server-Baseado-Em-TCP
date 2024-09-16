import socket, os

INTERFACE = '127.0.0.1'
PORT = 31435

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((INTERFACE, PORT))
server_socket.listen(1)

print(f"Servidor TCP escutando em {INTERFACE}:{PORT}...")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Conexão estabelecida com {client_address}")
    
    while True:
        command = client_socket.recv(1024).decode('utf-8')
        
        if command.startswith('UPLOAD'):
            filename = command.split(' ')[1]
            with open(filename, 'wb') as f:
                packet_num = 0
                while True:
                    data = client_socket.recv(4096)
                    if data == b'EOF':
                        break
                    packet_num += 1
                    f.write(data)
                    print(f'Recebendo pacote {packet_num}')
            print(f"Arquivo {filename} recebido com sucesso.")
        
        elif command.startswith('DOWNLOAD'):
            filename = command.split(' ')[1]
            try:
                with open(filename, 'rb') as f:
                    file_size = os.path.getsize(filename)
                    total_packet = file_size // 4096 + 1
                    packet_num = 0
                    while True:
                        data = f.read(4096)
                        if not data:
                            break
                        packet_num += 1
                        client_socket.sendall(data)
                        print(f'Enviado pacote {packet_num} de {total_packet}')
                print(f"Arquivo {filename} enviado com sucesso.")
            except FileNotFoundError:
                client_socket.sendall(b'ERROR: File not found')
        
        elif command == 'EXIT':
            break
    
    client_socket.close()
    print(f"Conexão com {client_address} encerrada.")
