import socket
import threading

HOST = '0.0.0.0'
PORT = 9000

sender = None
viewer = None

def handle_sender(conn):
    global viewer
    while True:
        data = conn.recv(4096)
        if not data:
            break
        if viewer:
            viewer.sendall(data)

def handle_viewer(conn):
    global sender
    while True:
        data = conn.recv(4096)
        if not data:
            break

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(2)

print("Relay server started")

while True:
    conn, addr = server.accept()
    role = conn.recv(10).decode()

    if role == "SENDER":
        sender = conn
        threading.Thread(target=handle_sender, args=(conn,)).start()
        print("Sender connected")

    elif role == "VIEWER":
        viewer = conn
        print("Viewer connected")
