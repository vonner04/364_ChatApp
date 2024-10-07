import socket
import threading
from database.client_manager import create_user_table, login_user

PORT = 5555
SERVER = socket.gethostbyname(socket.gethostname())


# Initialize the server
def start():
    create_user_table()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER, PORT))
    server_socket.listen(5)
    print(f"Server is listening on {SERVER}")

    while True:
        client_socket, address = server_socket.accept()
        print(f"Connection from {address} has been established.")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


def handle_client(client_socket):
    # Prompt user to login with username and password
    client_socket.send("[SERVER] Enter username: ".encode("utf-8"))
    username = client_socket.recv(1024).decode("utf-8")
    client_socket.send("[SERVER] Enter password: ".encode("utf-8"))
    password = client_socket.recv(1024).decode("utf-8")

    # Login user
    response = login_user(username, password)
    client_socket.send(response.encode("utf-8"))

    # Handle user requests
    while True:
        request = client_socket.recv(1024).decode("utf-8")

        if request == "exit":
            break

    client_socket.close()


if __name__ == "__main__":
    start()
