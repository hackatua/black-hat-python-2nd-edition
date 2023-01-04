import os
import paramiko
import socket
import sys
import threading

CWD = os.path.dirname(os.path.realpath(__file__))
HOSTKEY = paramiko.RSAKey(filename=os.path.join(CWD, 'test_rsa.key'))

class Server (paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, channel_id):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED

        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if username == 'tim' and password == 'sekret':
            return paramiko.AUTH_SUCCESSFUL

if __name__ == '__main__':
    server_ip = '0.0.0.0'
    server_port = 2222
    
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((server_ip, server_port))
        server_socket.listen(100)
        print('[+] Listening for connection ...')
        (client, addr) = server_socket.accept()
    except Exception as e:
        print('[-] Listen failed: %s' % str(e))
        sys.exit(1)
    else:
        print('[+] Got a connection!', client, addr)

    bhSession = paramiko.Transport(client)
    bhSession.add_server_key(HOSTKEY)
    server = Server()
    bhSession.start_server(server=server)

    channel = bhSession.accept(20)    
    if channel is None:
        print('*** No channel.')
        sys.exit(1)

    print('[+] Authenticated!')
    print(channel.recv(1024))
    channel.send('Welcome to bh_ssh')
    try:
        while True:
            command = input('Enter a command: ')
            if command != 'exit':
                channel.send(command)
                response = channel.recv(8192)
                print(response.decode())
            else:
                channel.send('exit')
                print('exiting')
                bhSession.close()
                break
    except KeyboardInterrupt:
        bhSession.close()