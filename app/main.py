
import socket


def main():
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    connection, address = server_socket.accept() # wait for client

    req = connection.recv(1024).decode() # receive data
    data = req.split("\r\n")
    endpoint = data[0].split(" ")[1]
   
    if endpoint == "/":
        response = "HTTP/1.1 200 OK\r\n\r\n".encode()
    elif endpoint.startswith("/echo/") :
        string = data[0].split(" ")[1].split("/")[2]
        response = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(string)}\r\n\r\n{string}'.encode()
    elif endpoint == "/user-agent":
        userAgent = data[3].split(": ")[1]
        response = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(userAgent)}\r\n\r\n{userAgent}'.encode()
    else:
        response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()   
    
    connection.send(response) # send response 
    connection.close() # close the connection after sending the response

if __name__ == "__main__":
    main()
