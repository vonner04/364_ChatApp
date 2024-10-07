import socket
import threading
from database.client_manager import create_user_table, login_user

PORT = 5555
SERVER = socket.gethostbyname(socket.gethostname())
EXIT_COMMAND = "!DISCONNECT"

# List of connected clients and their usernames
connected_clients = []
client_usernames = {}


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
        print(f"[SERVER] ACTIVE CONNECTIONS: {threading.activeCount() - 1}")


def handle_client(client_socket):
    try:
        if not login_process(client_socket):
            return

        # Notify others that a new client has joined
        broadcast(
            f"{client_usernames[client_socket]} has joined the chat", client_socket
        )

        # Handle requests from the client
        handle_requests(client_socket)

    except ConnectionResetError:
        print(f"Client {client_socket} disconnected unexpectedly")
        broadcast(f"{client_usernames[client_socket]} has left the chat", client_socket)
    finally:
        cleanup(client_socket)
        client_socket.close()
        print(f"Connection with {client_socket} has been closed")


def login_process(client_socket):
    while True:
        username = prompt(client_socket, "[SERVER] Enter a username: ")
        password = prompt(client_socket, "[SERVER] Enter a password: ")

        success, response = login_user(username, password)
        client_socket.send(response.encode("utf-8"))

        # If login is successful, store the client socket and username
        if success:
            client_usernames[client_socket] = username
            return True


def handle_requests(client_socket):
    connected_clients.append(client_socket)

    while True:
        request = client_socket.recv(1024).decode("utf-8")

        if request == EXIT_COMMAND:
            broadcast(
                f"{client_usernames[client_socket]} has left the chat", client_socket
            )
            break

        broadcast(f"{client_usernames[client_socket]}: {request}", client_socket)

    connected_clients.remove(client_socket)

    client_socket.close()


def prompt(client_socket, message):
    client_socket.send(message.encode("utf-8"))
    return client_socket.recv(1024).decode("utf-8")


def broadcast(message, current_client):
    sender_username = client_usernames[current_client]
    full_message = f"{sender_username}: {message}"

    for client in connected_clients:
        if client != current_client:
            try:
                client.send(full_message.encode("utf-8"))
            except socket.error:
                connected_clients.remove(client)
                if client in client_usernames:
                    del client_usernames[client]


def cleanup(client_socket):
    if client_socket in connected_clients:
        connected_clients.remove(client_socket)
    if client_socket in client_usernames:
        del client_usernames[client_socket]


if __name__ == "__main__":
    start()
