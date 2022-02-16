import socket
import threading
import base64
from queue import Queue
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from Crypto.Random import get_random_bytes

hostname = socket.gethostname()
HOST = socket.gethostbyname(hostname)
PORT = 10006
connected_clients = []
queue = Queue()
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def broadcast():
    while True:
        message, sender_socket = queue.get()
        user = ''
        for client_socket, username in connected_clients:
            if client_socket == sender_socket:
                user = username
                break

        for client_socket, _ in connected_clients:
            if client_socket != sender_socket:
                message = user + '<=>' + message.decode('utf-8')
                client_socket.send(message.encode('utf-8'))
        queue.task_done()


def sender():
    while True:
        message = input('> ')
        server_socket.send(message.encode('utf-8'))


def client_recv(client_socket):
    while True:
        data = client_socket.recv(1024)
        queue.put((data, client_socket))


def main():
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    broadcast_thread = threading.Thread(target=broadcast)
    broadcast_thread.start()
    username = input('Enter your username: ')
    print('Welcome', username)
    print(f'Chat Server active @{HOST}')
    print('Waiting for connections...')
    # "Type something, broadcast this to client"
    while True:
        client_socket, client_address = server_socket.accept()
        print(f'Got a connection from {client_address}')
        recv_thread = threading.Thread(target=client_recv, args=(client_socket,))
        recv_thread.start()


if __name__ == '__main__':
    main()
