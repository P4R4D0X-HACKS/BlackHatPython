import socket


target_host = "www.google.com"
target_port = 80

# Creating a client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to client
    client.connect((target_host, target_port))
    # Sending some data
    client.send(b"GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")
    # Receive some data
    response = client.recv(4096)
    # printing the response by decoding it
    print(response.decode())

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Closing the connection
    client.close()
