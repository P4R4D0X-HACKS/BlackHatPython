import socket


def main():
    target_host = "127.0.0.1"  # Change this to the server's IP if it's not running on the same machine
    target_port = 9998

    # Create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client.connect((target_host, target_port))
        print(f"[+] Connected to {target_host}:{target_port}")

        # Send some data
        message = "Hello, Server!"
        client.send(message.encode('utf-8'))
        print(f"[+] Sent: {message}")

        # Receive some data
        response = client.recv(4096)
        print(f"[+] Received: {response.decode('utf-8')}")

    except Exception as e:
        print(f"[-] An error occurred: {e}")

    finally:
        # Close the connection
        client.close()
        print("[+] Connection closed")


if __name__ == '__main__':
    main()
