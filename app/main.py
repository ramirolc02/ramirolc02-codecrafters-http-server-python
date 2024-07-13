import gzip
import os.path
import socket
import sys
from threading import Thread


def handle_compression(headers: str):
    supported = []
    for line in headers:
        if line.startswith("Accept-Encoding:"):
            compressionTypes = line.split(": ")[1].split(", ")
            supported = [compressionType for compressionType in compressionTypes if not compressionType.startswith("invalid-encoding")]
    return supported
  
            

def handle_request(connection, address):
    req = connection.recv(1024).decode() # receive data
    data = req.split("\r\n")
    type = data[0].split(" ")[0]
    endpoint = data[0].split(" ")[1]

    response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()   
    if endpoint == "/":
        response = "HTTP/1.1 200 OK\r\n\r\n".encode()
    elif endpoint.startswith("/echo/") :
        string = endpoint.split("/")[-1] # Last part of the endpoint
        compressionType: list[str] = handle_compression(data)
        encoding = ""
        if "gzip" in compressionType:
            encoding = f'Content-Encoding: gzip\r\n'
            string = gzip.compress(string.encode())
        response = f'HTTP/1.1 200 OK\r\n{encoding}Content-Type: text/plain\r\nContent-Length: {len(string)}\r\n\r\n{string}'.encode()
    elif endpoint == "/user-agent":
        for line in data:
            if line.startswith("User-Agent:"):
                userAgent = line.split(": ")[1]
                response = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(userAgent)}\r\n\r\n{userAgent}'.encode()
                break
    elif endpoint.startswith("/files/"):
        dir = sys.argv[2]
        filePath = f'{dir}/{endpoint[7:]}'
        if type == "POST":
            content = data[-1]
            with open(filePath, "w") as f:
                f.write(content)
            response = "HTTP/1.1 201 Created\r\n\r\n".encode()
        elif os.path.isfile(filePath):
            with open(filePath, "r") as f:
                content = f.read()
                print(content)
                response = f'HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(content)}\r\n\r\n{content}'.encode()

    connection.send(response) # send response 
    connection.close() # close the connection after sending the response
def main():
    print("Logs from your program will appear here!")
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        connection, address = server_socket.accept() # wait for client 
        thread = Thread(target=handle_request, args=(connection, address))
        thread.start()

if __name__ == "__main__":  
    main()
