import sys
import socket
import threading

HEX_FILTER = ''.join([(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)])


def hexdump(src: str, length: int = 16, show: bool = True) -> list[str]:
    """
    Display the hex representation of data.
    """
    if isinstance(src, bytes):
        src = src.decode()
    results = []
    for i in range(0, len(src), length):
        word = str(src[i:i+length])
        printable = word.translate(HEX_FILTER)
        hexa = ' '.join([f'{ord(c):02x}' for c in word])
        hex_width = length * 3
        results.append(f'{i:04x}   {hexa:<{hex_width}}   {printable}')
    if show:
        for line in results:
            print(line)
    else:
        return results


def receive_from(connection: socket.socket, timeout: int = 5) -> bytes:
    """
    Receive data from a connection with a specified timeout.
    """
    buffer = b""
    connection.settimeout(timeout)
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    except Exception:
        pass
    return buffer


def request_handler(buffer: bytes) -> bytes:
    """
    Modify the request packet if necessary.
    """
    # Perform packet modification here
    return buffer


def response_handler(buffer: bytes) -> bytes:
    """
    Modify the response packet if necessary.
    """
    # Perform packet modification here
    return buffer


def proxy_handler(client_socket: socket.socket, remote_host: str, remote_port: int, receive_first: bool):
    """
    Handle the proxying between the local client and the remote server.
    """
    # Create a socket to connect to the remote host
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    # If the receive_first flag is set, receive data from the remote host first
    if receive_first:
        remote_buffer = receive_from(remote_socket)
        if remote_buffer:
            print("[<==] Received %d bytes from remote." % len(remote_buffer))
            hexdump(remote_buffer)

            # Send the received data to the local client if there is any
            remote_buffer = response_handler(remote_buffer)
            client_socket.send(remote_buffer)

    # Loop to continuously read from local and remote sockets
    while True:
        # Receive data from the local client
        local_buffer = receive_from(client_socket)
        if local_buffer:
            print("[==>] Received %d bytes from localhost." % len(local_buffer))
            hexdump(local_buffer)

            # Send the data to the remote host
            local_buffer = request_handler(local_buffer)
            remote_socket.send(local_buffer)
            print("[==>] Sent to remote.")

        # Receive data from the remote host
        remote_buffer = receive_from(remote_socket)
        if remote_buffer:
            print("[<==] Received %d bytes from remote." % len(remote_buffer))
            hexdump(remote_buffer)

            # Send the data to the local client
            remote_buffer = response_handler(remote_buffer)
            client_socket.send(remote_buffer)
            print("[<==] Sent to localhost.")

        # If no more data, close the connections
        if not local_buffer and not remote_buffer:
            client_socket.close()
            remote_socket.close()
            print("[*] No more data. Closing connections.")
            break


def server_loop(local_host: str, local_port: int, remote_host: str, remote_port: int, receive_first: bool):
    """
    Setup and start the server to listen for incoming connections.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((local_host, local_port))
    except Exception as e:
        print("Problem on bind: %r" % e)
        print("[!!] Failed to listen on %s:%d" % (local_host, local_port))
        print("[!!] Check for other listening sockets or correct permissions.")
        sys.exit(0)
    print("[*] Listening on %s:%d" % (local_host, local_port))
    server.listen(5)
    while True:
        client_socket, addr = server.accept()
        print("> Received incoming connection from %s:%d" % (addr[0], addr[1]))

        # Start a new thread to handle the proxying for this connection
        proxy_thread = threading.Thread(
            target=proxy_handler,
            args=(client_socket, remote_host, remote_port, receive_first)
        )
        proxy_thread.start()


def main():
    """
    Main function to parse arguments and start the server loop.
    """
    if len(sys.argv[1:]) != 5:
        print("Usage: ./proxy.py [local_host] [local_port] [remote_host] [remote_port] [receive_first]")
        print("Example: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit(0)

    # Parse the command-line arguments
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])
    receive_first = sys.argv[5].lower() == 'true'

    # Start the server loop
    server_loop(local_host, local_port, remote_host, remote_port, receive_first)


if __name__ == '__main__':
    main()
