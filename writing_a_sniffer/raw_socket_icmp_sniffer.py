import socket
import os

HOST='0.0.0.0'

def isWindows():
    return os.name == 'nt'

def main():
    if isWindows():
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP

    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    sniffer.bind((HOST, 0))
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    if isWindows():
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    print(sniffer.recvfrom(65565))

    if isWindows():
        sniffer.setsockopt(socket.SIO_RCVALL, socket.RCVALL_OFF)

if __name__ == '__main__':
    main()
