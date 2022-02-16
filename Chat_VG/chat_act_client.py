import socket
import threading


HOST = '192.168.0.100'
PORT = 10006
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_username = ""


def sender():
    while True:
        message = input('> ')
        client_socket.send(message.encode('utf-8'))


def recv():
    while True:
        message = client_socket.recv(1024)
        message = message.decode('utf-8')
        print(f'{client_username}>>> {message}')


def main():

    client_username = input('Please enter your username: ')
    print(f'Welcome {client_username}!')
    client_socket.connect((HOST, PORT))
    client_socket.send(client_username.encode('utf-8'))
    s = threading.Thread(target=sender)
    r = threading.Thread(target=recv)
    s.start()
    r.start()

    s.join()
    r.join()


if __name__ == '__main__':
    main()
