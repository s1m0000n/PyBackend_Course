"""Simple client for testing client-server socket app"""
import sys
import socket


if __name__ == '__main__':
    try:
        request = sys.argv[1]
    except IndexError:
        print('Expected request as the 1st arg')
        sys.exit()
    else:
        sock = socket.socket()
        try:
            sock.connect(('127.0.0.1', 5000))
        except ConnectionRefusedError:
            print('Could not connect to the server')
            sys.exit()
        sock.sendall(request.encode('utf-8'))
        data = sock.recv(1024)
        sock.close()
        print(data.decode('utf-8'))
