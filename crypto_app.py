import os.path

from Crypto.PublicKey.RSA import RsaKey
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA


# AES------------------------------------------------------------------------------------------------
def aes_encrypt(message):
    # Generate a random 128-bit (16 bytes) key, used for encryption/decryption
    key = get_random_bytes(16)

    # Create an AES object
    cipher_aes = AES.new(key, AES.MODE_EAX)

    # Encrypt
    # Return the encrypted message and the MAC tag (hash value) of the message
    cipher_text, tag = cipher_aes.encrypt_and_digest(message.encode('utf-8'))

    return key, cipher_text, cipher_aes.nonce, tag


def aes_decrypt(aes_key, cipher_text, nonce, tag):
    # Create an AES object
    cipher_aes = AES.new(aes_key, AES.MODE_EAX, nonce)
    decrypted_data = cipher_aes.decrypt_and_verify(cipher_text, tag)

    return decrypted_data.decode('utf-8')


# RSA------------------------------------------------------------------------------------------------
def generate_rsa_keys(key_name, key_size=2048):
    # Generate a key-pair with the specified key size
    key = RSA.generate(key_size)

    # Extract the private key
    private_key = key.export_key()
    with open(f'./rsa_keys/{key_name}_private.pem', 'wb') as out_file:
        out_file.write(private_key)

    # Extract the public key
    public_key = key.public_key().export_key()
    with open(f'./rsa_keys/{key_name}_public.pem', 'wb') as out_file:
        out_file.write(public_key)


# Encrypt with RSA-----------------------------------------------------------------------------------
def rsa_encrypt(rsa_key_name, message):
    recipient_key = RSA.importKey(open(f'./rsa_keys/{rsa_key_name}.pem').read())
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    return cipher_rsa.encrypt(message)
    # return cipher_rsa.encrypt(message.encode('utf-8'))


# Decrypt with RSA-----------------------------------------------------------------------------------
def rsa_decrypt(cipher, recipient_key):
    if type(recipient_key) != RsaKey:
        # If there is a key, open and read
        if os.path.isfile(f'./rsa_keys/{recipient_key}.pem'):
            recipient_key = RSA.importKey(open(f'./rsa_keys/{recipient_key}.pem').read())
        # Else print out message
        else:
            print(f'No key file named {recipient_key}.pem found')
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    return cipher_rsa.decrypt(cipher)
    # return cipher_rsa.decrypt(cipher).decode('utf-8')


def encrypt_message(message, recipient_rsa_key_name):
    # Encrypt message using AES
    aes_key, aes_cipher, aes_nonce, aes_tag = aes_encrypt(message)

    # Encrypt generated AES key using RSA
    encrypted_aes_key = rsa_encrypt(recipient_rsa_key_name, aes_key)
    return (encrypted_aes_key, aes_nonce, aes_tag, aes_cipher)


def decrypt_message(private_key_name, encrypted_data):
    # Extract encrypted data
    encrypted_aes_key, aes_nonce, aes_tag, aes_cipher = encrypted_data

    # Decrypt the AES key using RSA
    aes_key = rsa_decrypt(encrypted_aes_key, private_key_name)

    # Decrypt the message using AES
    plain_text = aes_decrypt(aes_key, aes_cipher, aes_nonce, aes_tag)

    return plain_text

def main():
    # We maintain a secure way of sending our 'aes_key' and 'aes_nonce' by using RSA
    # aes_key, aes_cipher, aes_nonce, aes_tag = aes_encrypt('This is a secret message')
    # message = aes_decrypt(aes_key, aes_cipher, aes_nonce, aes_tag)
    # print(message)
    generate_rsa_keys('niclas')
    # rsa_cipher = rsa_encrypt('niclas_public', 'Oi oi mate')
    # message = rsa_decrypt(rsa_cipher, 'niclas_private')
    # print(message)

    # # Sender Code
    # message = input('Message to encrypt: ')
    # recipient_key_name = input('Public key name of recipient: ')
    # encrypted_data = encrypt_message(message, recipient_key_name)
    #
    # # Receiver Code
    # private_key = input('Private key name to be used for encryption: ')
    # plain_text_message = decrypt_message(private_key, encrypted_data)
    # print(plain_text_message)


if __name__ == '__main__':
    main()
