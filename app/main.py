
import socket


def main():
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    connection, address = server_socket.accept() # wait for client

    req = connection.recv(1024).decode() # receive data
    data = req.split("\r\n")

    response = "HTTP/1.1 200 OK\r\n\r\n".encode()
    if data[0].split(" ")[1] != "/":
        response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()   
    connection.send(response) # send response 
    connection.close() # close the connection after sending the response

if __name__ == "__main__":
    main()
