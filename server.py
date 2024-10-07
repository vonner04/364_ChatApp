import socket
import threading
from database.client_manager import create_user_table, login_user
from broadcaster import Broadcaster

PORT = 5555
SERVER = socket.gethostbyname(socket.gethostname())
EXIT_COMMAND = "!DISCONNECT"


# Initialize the server
def start():
    create_user_table()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER, PORT))
    server_socket.listen(5)
    print(f"Server is listening on {SERVER}")

    # Initialize the broadcaster
    broadcaster = Broadcaster()

    while True:
        client_socket, address = server_socket.accept()
        print(f"Connection from {address} has been established.")
        client_handler = threading.Thread(
            target=handle_client, args=(client_socket, broadcaster)
        )
        client_handler.start()
        print(f"[SERVER] ACTIVE CONNECTIONS: {threading.active_count() - 1}")


# Function to handle a client connection
def handle_client(client_socket, broadcaster):
    try:
        if not login_process(client_socket, broadcaster):
            return

        # Notify others that a new client has joined
        broadcaster.broadcast(
            f"{broadcaster.client_usernames[client_socket]} has joined the chat",
            client_socket,
        )

        # Handle requests from the client
        handle_requests(client_socket, broadcaster)

    except ConnectionResetError:
        print(
            f"Client {broadcaster.client_usernames[client_socket]} disconnected unexpectedly"
        )
        broadcaster.broadcast(
            broadcaster.broadcast(
                f"{broadcaster.client_usernames[client_socket]} has left the chat",
                client_socket,
            )
        )
    finally:
        broadcaster.remove_client(client_socket)
        client_socket.close()
        print(f"Connection with {client_socket} has been closed")


def login_process(client_socket, broadcaster):

    while True:
        username = prompt(client_socket, "[SERVER] Enter a username: ")
        password = prompt(client_socket, "[SERVER] Enter a password: ")

        success, response = login_user(username, password)
        client_socket.send(response.encode("utf-8"))

        # If login is successful, store the client socket and username
        if success:
            broadcaster.add_client(client_socket, username)
            return True


def handle_requests(client_socket, broadcaster):

    while True:
        request = client_socket.recv(1024).decode("utf-8")

        if request == EXIT_COMMAND:
            broadcaster.broadcast(
                f"{broadcaster.client_usernames[client_socket]} has left the chat",
                client_socket,
            )
            break

    broadcaster.remove_client(client_socket)

    client_socket.close()


def prompt(client_socket, message):
    client_socket.send(message.encode("utf-8"))
    return client_socket.recv(1024).decode("utf-8")


if __name__ == "__main__":
    start()
