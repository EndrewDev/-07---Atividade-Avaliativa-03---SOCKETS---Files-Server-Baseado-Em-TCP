import socket, os

SERVER_ADDRESS = '127.0.0.1'
PORT = 31435

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_ADDRESS, PORT))

command = input("Digite o comando (UPLOAD/DOWNLOAD) e o nome do arquivo: ")
client_socket.sendall(command.encode('utf-8'))

if command.startswith('UPLOAD'):
    filename = command.split(' ')[1]
    try:
        with open(filename, 'rb') as f:
            file_size = os.path.getsize(filename)
            total_packets = file_size // 4096 + 1
            packet_num = 0
            while True:
                data = f.read(4096)
                if not data:
                    client_socket.sendall(b'EOF')
                    break
                packet_num += 1
                client_socket.sendall(data)
                print(f'Enviado pacote {packet_num} de {total_packets}')
        print(f"Arquivo {filename} enviado com sucesso.")
    except FileNotFoundError:
        print(f"Arquivo {filename} não encontrado.")
    
elif command.startswith('DOWNLOAD'):
    filename = command.split(' ')[1]

    if os.path.exists(filename):
        base, ext = os.path.splitext(filename)
        new_filename = f'{base}_novo{ext}'
        filename = new_filename

    received_data = b''
    packet_num = 0
    while True:
        data = client_socket.recv(4096)
        if data == b'EOF':
            break
        packet_num += 1
        print(f'Recebendo pacote {packet_num}')
        received_data += data
    
    with open(f"baixado_{filename}", 'wb') as f:
        f.write(received_data)
    print(f"Arquivo {filename} baixado com sucesso.")

client_socket.close()