import os
import re
import socket
import threading

domain = 'http://www.example.com'  #the domain name
home ='/home'  #the root directory for file server
host = '192.168.25.47'
port = 80

def full_path(path):
    path = path.split('/')
    return '<span>&emsp;&emsp;</span><span><a href="/">home</a></span><span>/</span>' + ''.join(['<span><a href="%s">%s</a></span><span>/</span>'%('/'.join(path[:i+1]), directory) for i, directory in enumerate(path[:-1])]) + '<span>%s</span>'%path[-1]

def handle(conn):
    path = re.search('GET /(.*?) ', conn.recv(1024).decode()).group(1)
    abs_path = os.path.join(home, path)
    if os.path.isfile(abs_path):
        with open(abs_path, 'rb') as file:
            data = file.read()
        conn.sendall(('HTTP/1.1 200 OK\r\nAccept-Ranges: bytes\r\nContent-Length: %d\r\nContent-Type: application/x-download\r\nContent-Disposition: attachment;filename=%s\r\nConnection: keep-alive\n\n'%(len(data), path.split('/')[-1])).encode() + data)
    elif os.path.isdir(abs_path):
        conn.sendall(html.format(full_path(path), ''.join(['<li><a href="%s">%s</a></li>'%(path + '/' +  item, item) for item in os.listdir(abs_path)])).encode())
    conn.close()

html = 'HTTP/1.1 200 OK\r\nAccept-Ranges: bytes\r\nContent-Type: text/html; charset=utf-8\n\n<!DOCTYPE HTML><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"><title>My Directory</title><base href="%s" /><style>span{{float:left}}</style></head><body style="font-family:Arial,Helvetica"><h1>&emsp;Directory listing</h1><div>{}</div><br><br><hr><ul>{}</ul><hr></body></html>'%domain
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(8)
while True:
    conn, _ = s.accept()
    threading.Thread(target=handle, args=(conn,)).start()
