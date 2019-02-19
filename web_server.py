import os
import re
import socket
import threading

content_type = {'html': 'text/html', 'htm': 'text/html', 'jsp': 'text/html', 'xhtml': 'text/html', 'js': 'application/x-javascript', 'css': 'text/css', 'tif': 'image/tiff', 'gif': 'image/giff', 'ico': 'image/icon', 'jpg': 'image/jpeg', 'png': 'image/png'}
home = '/home'  #the root directory for website
host = '192.168.25.47'
port = 80

def handle(conn):
    path = re.search('GET /(.*?) ', conn.recv(1024).decode()).group(1)
    if path == '':
        path = 'index.html'  #default page
    abs_path = os.path.join(home, path)
    if os.path.isfile(abs_path):
        with open(abs_path, 'rb') as file:
            content = file.read()
        extension = path.split('.')[-1]
        if extension in content_type.keys():
            conn.sendall(('HTTP/1.1 200 OK\r\nContent-Type: %s\n\n'%content_type[extension]).encode() + content)
        else:
            conn.sendall(('HTTP/1.1 200 OK\r\nAccept-Ranges: bytes\r\nContent-Length: %d\r\nContent-Type: application/x-download\r\nContent-Disposition: attachment;filename=%s\n\n'%(len(content), path.split('/')[-1])).encode() + content)
    else:
        conn.sendall('HTTP/1.1 404\n\n 404 Not Found'.encode())  #404 page
    conn.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(8)
while True:
    conn, _ = s.accept()
    threading.Thread(target=handle, args=(conn,)).start()
