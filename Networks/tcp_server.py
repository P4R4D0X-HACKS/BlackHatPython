import socket
import threading

IP = "0.0.0.0"
PORT = 9998


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT))
    server.listen(5)  # Start listening with a backlog of 5 connections
    print(f'[+] Listening on {IP}:{PORT}')

    try:
        while True:
            client, address = server.accept()
            print(client)
            print(f"[+] Accepted connection from {address[0]}:{address[1]}")
            client_handler = threading.Thread(target=handle_client, args=(client,))
            client_handler.start()
    except KeyboardInterrupt:
        print("\n[+] Shutting down the server.")
    finally:
        server.close()


def handle_client(client_socket):
    with client_socket as sock:
        try:
            request = sock.recv(1024)
            print(f"[+] Received: {request.decode('utf-8')}")
            sock.send(b'ACK')
        except Exception as e:
            print(f"[-] Error handling client: {e}")


if __name__ == '__main__':
    main()
