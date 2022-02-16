import socket
import threading


HOST = '192.168.0.100'
PORT = 10007
CLIENT_USERNAME = "CLIENT"


def sender(client_socket):
    while True:
        message = input('> ')
        client_socket.send(message.encode('utf-8'))


def main():

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    print(f'Welcome {CLIENT_USERNAME}!')
    input_thread = threading.Thread(target=sender, args=(client_socket,))
    input_thread.start()
    input_thread.join()

    while True:
        message = client_socket.recv(1024)
        message = message.decode('utf-8')
        print(message)


if __name__ == '__main__':
    main()
