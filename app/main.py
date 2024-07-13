

import os.path
import socket
import sys
from threading import Thread


def handle_request(connection, address,dir):
    req = connection.recv(1024).decode() # receive data
    data = req.split("\r\n")
    endpoint = data[0].split(" ")[1]
    response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()   

    if endpoint == "/":
        response = "HTTP/1.1 200 OK\r\n\r\n".encode()
    elif endpoint.startswith("/echo/") :
        string = endpoint.split("/")[2]
        response = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(string)}\r\n\r\n{string}'.encode()
    elif endpoint == "/user-agent":
        for line in data:
            if line.startswith("User-Agent:"):
                userAgent = line.split(": ")[1]
                response = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(userAgent)}\r\n\r\n{userAgent}'.encode()
                break
    elif endpoint.startswith("/files/"):
        filePath = f'{dir}/{endpoint.split("/")[2]}'
        if os.path.isfile(filePath):
            with open(filePath, "r") as f:
                content = f.read()
                print(content)
                response = f'HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(content)}\r\n\r\n{content}'.encode()

    connection.send(response) # send response 
    connection.close() # close the connection after sending the response
def main():
    print("Logs from your program will appear here!")
    dir = None
    flag = sys.argv[1] if len(sys.argv) > 2 else []
    if "--directory" in flag:
        dir = sys.argv[2]

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        connection, address = server_socket.accept() # wait for client
        if dir: 
            thread = Thread(target=handle_request, args=(connection, address, dir))
        else: 
            thread = Thread(target=handle_request, args=(connection, address))
        thread.start()

if __name__ == "__main__":  
    main()
