import base64
import socket
import threading
from queue import Queue
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from Crypto.Random import get_random_bytes

hostname = socket.gethostname()
HOST = socket.gethostbyname(hostname)
PORT = 9876
server_username = "alice"
connected_clients = []
broadcast_queue = Queue()
SESSION_KEY = get_random_bytes(16)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def main():
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    broadcast_thread = threading.Thread(target=broadcast)
    broadcast_thread.start()

    print(f'Chat Server hosted at: {HOST}:{PORT}')
    print('Waiting for connections...')

    while True:
        client_socket, client_address = server_socket.accept()
        print(f'Got a connection from {client_address}')
        if handshake(client_socket):
            print(f'HANDSHAKE with {client_address} OK!')
            client_thread = threading.Thread(target=client_handler, args=(client_socket,))
            client_thread.start()
        else:
            print(f'Invalid handshake with {client_address}.')

        aes_cipher = AES.new(SESSION_KEY, AES.MODE_EAX)
        message = input('> ')
        cipher_text, tag = aes_cipher.encrypt_and_digest(message.encode('utf-8'))
        nonce = base64.b64encode(aes_cipher.nonce).decode('utf-8')
        tag = base64.b64encode(tag).decode('utf-8')
        cipher_text = base64.b64encode(cipher_text).decode('utf-8')
        encrypted_message = ','.join((nonce, tag, cipher_text))
        client_socket.send(encrypted_message.encode('utf-8'))


def read_public_key(key_name):
    return RSA.importKey(open(f'./rsa_keys_chat/{key_name}_pub.key', 'r').read())


def client_handler(client_socket):
    from chat_act_client import username
    while True:
        message = client_socket.recv(1024)
        nonce, tag, cipher_text = message.decode('utf-8').split(',')
        nonce = base64.b64decode(nonce)
        tag = base64.b64decode(tag)
        cipher_text = base64.b64decode(cipher_text)

        aes_cipher = AES.new(SESSION_KEY, AES.MODE_EAX, nonce)
        clear_text = aes_cipher.decrypt_and_verify(cipher_text, tag)

        clear_text = clear_text.decode('utf-8')
        print(f'{username}:{clear_text}')



def broadcast():
    while True:
        message, sender_socket = broadcast_queue.get()
        user = ''
        for client_socket, username in connected_clients:
            if client_socket == sender_socket:
                user = username
                break

        for client_socket, _ in connected_clients:
            if client_socket != sender_socket:
                message = user + '<=>' + message.decode('utf-8')

                aes_cipher = AES.new(SESSION_KEY, AES.MODE_EAX)
                cipher_text, tag = aes_cipher.encrypt_and_digest(message.encode('utf-8'))

                nonce = base64.b64encode(aes_cipher.nonce).decode('utf-8')
                tag = base64.b64encode(cipher_text).decode('utf-8')

                encrypted_message = (nonce, tag, cipher_text)
                client_socket.send(encrypted_message.encode('utf-8'))
            broadcast_queue.task_done()


def handshake(client_socket):
    confirmation_bytes = get_random_bytes(16)
    username = client_socket.recv(1024).decode('utf-8')
    hashed_bytes = SHA256.new(confirmation_bytes)
    client_socket.send(confirmation_bytes)
    confirmation_data = client_socket.recv(1024)
    public_key = read_public_key(username)

    try:
        pkcs1_15.new(public_key).verify(hashed_bytes, confirmation_data)
        rsa_cipher = PKCS1_OAEP.new(public_key)
        client_socket.send('Welcome'.encode('utf-8'))
        encrypted_session_key = rsa_cipher.encrypt(SESSION_KEY)
        client_socket.send(encrypted_session_key)
        connected_clients.append((client_socket, username))
        return True

    except (ValueError, TypeError):
        client_socket.send("Couldn't approve client. Terminating".encode('utf-8'))

    return False


if __name__ == '__main__':
    main()
