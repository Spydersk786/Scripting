import socket

ip_addr='192.168.0.23'
port=444
# # for TCP
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# for UDP
# client=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

# Only required for TCP as UDP need not to connect
client.connect((ip_addr,port))

# # function to send data via TCP
client.send(b"hello")

# function to send data via UDP
# client.sendto(b"hello", (ip_addr, port))

# Receive a response from the server
response=client.recv(1024)  
print(f"Received: {response.decode('utf-8')}")

#always close the client
client.close()