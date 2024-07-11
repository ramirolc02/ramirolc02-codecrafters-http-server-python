
import socket


def main():
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    connection, address = server_socket.accept() # wait for client
    receive = connection.recv(1024) # receive data
    if receive.split()[0] == b"GET / HTTP/1.1":
        connection.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
    else:
        connection.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")

if __name__ == "__main__":
    main()
