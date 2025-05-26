import socket
import ssl
import os
from Crypto.Cipher import AES

PATH = os.path.dirname(os.path.abspath(__file__))


def main():
    context = ssl._create_unverified_context(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations(r"C:\Users\anger\Downloads\server.crt")

    sock = socket.socket()
    ssock = context.wrap_socket(sock)

    while True:
        try:
            ssock.connect(("127.0.0.1", 42069))

            key = os.urandom(16)
            with open(f"{PATH}/key.txt", 'w') as key_file:
                key_file.write(str(key))
            ssock.send(key)

            folder_path = input("enter folder path: ")
            ssock.send((folder_path).encode())

            print(ssock.recv(1024).decode())

            ssock.close()
            break

        except:
            pass


if __name__ == '__main__':
    main()