import socket
import threading
import queue

hostname = socket.gethostname()
HOST = socket.gethostbyname(hostname)
PORT = 9876
connected_clients = []
server_username = "Bob"
client_username = ""


def client_handler(client_socket, broadcast_queue, client_list):
    from chat_act_client import client_username
    while True:
        try:
            message = client_socket.recv(1024)
            message = message.decode('utf-8')
            print(f'{client_username}: {message}')

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
    global server_username, client_username
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f'Chat Server hosted at: {HOST}:{PORT}')
    print('Waiting for connections...')
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    client_socket, client_address = server_socket.accept()
    client_list = []
    broadcast_queue = queue.Queue()
    print(f'Got a connection from {client_address}')

    while True:
        broadcast_thread = threading.Thread(target=broadcast, args=(client_list, broadcast_queue))
        broadcast_thread.start()
        client_message = input('> ')
        client_message = client_message.encode('utf-8')
        client_socket.send(client_message)
        client_thread = threading.Thread(target=client_handler,
                                         args=(client_socket, broadcast_queue, client_list))
        client_list.append(client_socket)
        client_thread.start()


if __name__ == '__main__':
    main()
