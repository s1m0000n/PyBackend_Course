from multiprocessing import Pool
import sys
import socket
from time import sleep


def process_url(url: str):
    sock.send(url.replace('\n', '').encode(sys.stdout.encoding))
    print(url.replace('\n', '').encode(sys.stdout.encoding))
    sleep(1)
    data = sock.recv(4096)
    result = data.decode(sys.stdout.encoding)
    print(result)
    return


f = open('urls.txt', 'r')
sock = socket.socket()
sock.connect(('127.0.0.1', 5051))
with Pool(1) as p:
    p.map(process_url, f.readlines())
