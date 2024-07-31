import socket

target_host = "0.0.0.0"
target_port = 9998

# Create a UDP socket
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    # Send some data
    client.sendto(b"HELLO HACKER", (target_host, target_port))

    # Receive response
    data, addr = client.recvfrom(4096)
    print(f"Received {data.decode()} from {addr}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    client.close()
