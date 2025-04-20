import socket

def main():
    # Create a UDP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to an IP and port
    server.bind(("0.0.0.0", 444))  # Listen on all interfaces, port 444

    while True:
        # Wait for data from any client
        data, addr = server.recvfrom(1024)  # buffer size is 1024 bytes
        print(f"Received from {addr}: {data.decode()}")
        # Send a response back to the client
        server.sendto(b"Hello from UDP server!", addr)

if __name__ == "__main__":
    main()
