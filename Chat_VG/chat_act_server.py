import socket
import threading
import queue
from chat_act_client import CLIENT_USERNAME

hostname = socket.gethostname()
HOST = socket.gethostbyname(hostname)
PORT = 10007
connected_clients = []
USERNAME = "HOST"


def client_handler(client_socket, broadcast_queue, client_list):
    while True:
        try:
            message = client_socket.recv(1024)
            message = message.decode('utf-8')
            print('CLIENT > ', message)

            message_dict = {
                'sender_socket': client_socket,
                'message': message.encode('utf-8')
            }
            broadcast_queue.put(message_dict)
        except ConnectionResetError:
            print('A client left the chat')
            client_list.remove(client_socket)
            break


def broadcast(client_list, broadcast_queue):
    while True:
        message_dict = broadcast_queue.get()
        for client in client_list:
            if client != message_dict['sender_socket']:
                client.send(message_dict['message'])


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    client_list = []
    broadcast_queue = queue.Queue()

    broadcast_thread = threading.Thread(target=broadcast, args=(client_list, broadcast_queue))
    broadcast_thread.start()
    print('Welcome', USERNAME)
    print(f'Chat Server @{HOST}')
    print('Waiting for connections...')

    while True:
        client_socket, client_address = server_socket.accept()
        print(f'Got a connection from {client_address}')
        client_thread = threading.Thread(target=client_handler,
                                         args=(client_socket, broadcast_queue, client_list))
        client_list.append(client_socket)
        client_thread.start()
        client_thread.join()



if __name__ == '__main__':
    main()
