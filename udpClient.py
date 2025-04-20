import socket

ip_addr='192.168.0.14'
port=444

# for UDP
client=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

# function to send data via UDP
client.sendto(b"hello", (ip_addr, port))

# Receive a response from the server
response,ip_addr=client.recvfrom(1024)  
print(f"Received from {ip_addr}: {response.decode('utf-8')}")

#always close the client
client.close()