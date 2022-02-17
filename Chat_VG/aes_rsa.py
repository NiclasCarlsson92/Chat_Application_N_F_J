from Crypto.PublicKey import RSA


def gen_keys(key_name, passphrase, key_size):
    key = RSA.generate(key_size)
    public_key = key.publickey().export_key()
    private_key = key.export_key(passphrase=passphrase, pkcs=8, protection='scryptAndAES128-CBC')

    with open(f'./rsa_keys_chat/{key_name}_pub.key', 'wb') as pub_file:
        pub_file.write(public_key)

    with open(f'./rsa_keys_chat/{key_name}_priv.key', 'wb') as priv_file:
        priv_file.write(private_key)


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



def menu():
    while True:
        print('>>>>> ENCRYPTION MENU <<<<<')
        print('===========================')
        print('1. Generate RSA keys')
        choice = input('> ')

        if choice == '1':
            generate_keys()
            break


def main():
    menu()


if __name__ == '__main__':
    main()
