import socket
import threading

# 0.0.0.0 is from all
# 192.168.x.x from this network
# 127.0.0.1 from local host
ip_addr_to_accept_connection_from='0.0.0.0'
port=444

def main():
    server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket
    # Bind the server to the IP address and port
    server.bind((ip_addr_to_accept_connection_from, port))
    server.listen(5)  # Listen for incoming connections only for tcp

    while True:
        client,addr=server.accept()  # Accept a connection
        print(f"Connection from {addr} has been established!")
        # Start a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client,))
        client_thread.start()

def handle_client(client_socket):
    with client_socket as sock:
        request = sock.recv(1024)
        print(f"Received: {request.decode('utf-8')}")
        # Send a response back to the client
        sock.send(b"ACK")

if __name__ == '__main__':
    main()