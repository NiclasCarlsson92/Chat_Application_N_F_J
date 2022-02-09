import os
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes


def gen_keys(key_name, passphrase, key_size):
    key = RSA.generate(key_size)
    public_key = key.publickey().export_key()
    private_key = key.export_key(passphrase=passphrase, pkcs=8, protection='scryptAndAES128-CBC')

    with open(f'{key_name}_pub.key', 'wb') as pub_file:
        pub_file.write(public_key)

    with open(f'{key_name}_priv.key', 'wb') as priv_file:
        priv_file.write(private_key)


def read_public_key(key_name):
    return RSA.importKey(open(f'{key_name}_pub.key', 'r').read())


def read_private_key(key_name, passphrase):
    return RSA.importKey(open(f'{key_name}_priv.key', 'r').read(), passphrase)


def generate_keys():
    key_name = input('Please enter a name for this key pair: ')
    while True:
        passphrase = input('Enter passphrase for private key: ')
        passphrase_repeat = input('Please repeat the passphrase: ')
        if passphrase != passphrase_repeat:
            print('Passphrases does not match. Try again.')
            continue
        break
    while True:
        key_size = input('Enter desired key size: ')
        if not key_size.isdecimal():
            print('Please enter key size using digits only. Try again.')
            continue
        break
    key_size = int(key_size)

    gen_keys(key_name, passphrase, key_size)


def encrypt_message():
    message = input('Enter message to encrypt: ').encode('utf-8')
    while True:
        key_name = input('Enter name of recipient: ')
        if not os.path.exists(f'{key_name}_pub.key'):
            print(f'Can\'t find key file named {key_name}_pub.key. Please try again.')
            continue
        break

    public_key = read_public_key(key_name)

    encrypted_file_name = input('Enter file name for encrypted message: ')

    # Create a session key that will be used with AES to encrypt the message
    session_key = get_random_bytes(16)

    # Encrypt the session key using RSA
    rsa_cipher = PKCS1_OAEP.new(public_key)
    encrypted_session_key = rsa_cipher.encrypt(session_key)

    # Encrypt the message using AES and the session key
    aes_cipher = AES.new(session_key, AES.MODE_EAX)
    cipher_text, tag = aes_cipher.encrypt_and_digest(message)

    values = [encrypted_session_key, aes_cipher.nonce, tag, cipher_text]
    with open(encrypted_file_name + '.enc', 'wb') as out_file:
        for value in values:
            out_file.write(value)
    print(f'The encrypted message was saved in the file {encrypted_file_name}.enc')


def decrypt_message():
    while True:
        file_name = input('Please enter the name of the encrypted message: ')
        if not os.path.exists(f'{file_name}.enc'):
            print(f'Can\'t find file named {file_name}.enc. Please try again.')
            continue
        break
    private_key_name = input('Enter the name of the private key to use: ')
    passphrase = input('Enter the passphrase used for this key: ')

    private_key = read_private_key(private_key_name, passphrase)
    with open(f'{file_name}.enc', 'rb') as in_file:
        enc_session_key, nonce, tag, cipher_text = [in_file.read(b) for b in (private_key.size_in_bytes(), 16, 16, -1)]

    # Decrypt the session key
    rsa_cipher = PKCS1_OAEP.new(private_key)
    session_key = rsa_cipher.decrypt(enc_session_key)

    # Decrypt the message
    aes_cipher = AES.new(session_key, AES.MODE_EAX, nonce)
    message = aes_cipher.decrypt_and_verify(cipher_text, tag)
    print("The decrypted message is:")
    print(message.decode('utf-8'))


def menu():
    while True:
        print('>>>>> ENCRYPTION MENU <<<<<')
        print('===========================')
        print('1. Generate RSA keys')
        print('2. Encrypt message')
        print('3. Decrypt message')
        print()
        print('9. Exit')
        choice = input('> ')

        if choice == '1':
            generate_keys()
        elif choice == '2':
            encrypt_message()
        elif choice == '3':
            decrypt_message()
        elif choice == '9':
            break


def main():
    menu()


if __name__ == '__main__':
    main()