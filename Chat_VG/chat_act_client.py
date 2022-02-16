import socket
import threading

LOCALHOST = ""
HOST = '192.168.0.100'
PORT = 9876
client_username = "Alice"
server_username = ""
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def send(client_socket):
    while True:
        message = input('> ')
        client_socket.send(message.encode('utf-8'))


def recv(client_socket):
    from chat_act_server import server_username
    while True:
        message = client_socket.recv(1024)
        message = message.decode('utf-8')
        print(f'{server_username}:{message}')


def main():
    global client_username
    client_socket.connect((HOST, PORT))
    print("Chat is connected")
    from chat_act_server import server_username
    while True:
        message = client_socket.recv(1024)
        message = message.decode('utf-8')
        input_thread_send = threading.Thread(target=send, args=(client_socket,))
        input_thread_recv = threading.Thread(target=recv, args=(client_socket,))
        input_thread_send.start()
        input_thread_recv.start()
        print(f'{server_username}:{message}')


if __name__ == '__main__':
    main()
