import socket
import sys
import threading
import base64
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15

HOST = '192.168.0.100'
PORT = 9876
username = "niclas"
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def read_private_key(key_name, passphrase):
    return RSA.importKey(open(f'./rsa_keys_chat/{key_name}_priv.key', 'r').read(), passphrase)


def main():
    passphrase = input('Enter your passphrase: ')
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    client_socket.send(username.encode('utf-8'))
    confirmation_bytes = client_socket.recv(1024)

    private_key = read_private_key(username, passphrase)

    hashed_bytes = SHA256.new(confirmation_bytes)
    signature = pkcs1_15.new(private_key).sign(hashed_bytes)
    client_socket.send(signature)

    response = client_socket.recv(1024).decode('utf-8')
    if response != "Welcome":
        print(response)
        sys.exit()
    encrypted_session_key = client_socket.recv(1024)

    rsa_cipher = PKCS1_OAEP.new(private_key)
    session_key = rsa_cipher.decrypt(encrypted_session_key)
    print('Connection is OK, SESSION LIVE!')

    def send():
        while True:
            aes_cipher = AES.new(session_key, AES.MODE_EAX)
            message = input('> ')
            cipher_text, tag = aes_cipher.encrypt_and_digest(message.encode('utf-8'))
            nonce = base64.b64encode(aes_cipher.nonce).decode('utf-8')
            tag = base64.b64encode(tag).decode('utf-8')
            cipher_text = base64.b64encode(cipher_text).decode('utf-8')
            encrypted_message = ','.join((nonce, tag, cipher_text))
            client_socket.send(encrypted_message.encode('utf-8'))

    def recv():
        from chat_act_server import server_username
        while True:
            message = client_socket.recv(1024)
            nonce, tag, cipher_text = message.decode('utf-8').split(',')
            nonce = base64.b64decode(nonce)
            tag = base64.b64decode(tag)
            cipher_text = base64.b64decode(cipher_text)

            aes_cipher = AES.new(session_key, AES.MODE_EAX, nonce)
            clear_text = aes_cipher.decrypt_and_verify(cipher_text, tag)

            message = clear_text.decode('utf-8')
            print(f'{server_username}:{message}')

    input_thread_send = threading.Thread(target=send)
    input_thread_recv = threading.Thread(target=recv)
    input_thread_send.start()
    input_thread_recv.start()
    input_thread_send.join()
    input_thread_recv.join()


if __name__ == '__main__':
    main()
