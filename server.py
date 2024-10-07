import socket
import threading
from database.client_manager import create_user_table, login_user
from broadcaster import Broadcaster

PORT = 5555
SERVER = socket.gethostbyname(socket.gethostname())
EXIT_COMMAND = "!DISCONNECT"
broadcaster = Broadcaster()


# Initialize the server
def start():
    create_user_table()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER, PORT))
    server_socket.listen(5)
    print(f"Server is listening on {SERVER}")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connection from {addr} has been established.")
        client_handler = threading.Thread(target=handle_client, args=(conn, addr))
        client_handler.start()
        print(f"[SERVER] ACTIVE CONNECTIONS: {threading.active_count() - 1}")


# Function to handle a client connection
def handle_client(conn, addr):

    # Limit the number of clients to 2
    if threading.active_count() - 1 > 2:
        conn.send("Server is full. Try again later.".encode("utf-8"))
        conn.close()
        return

    authenticated = False
    username = None

    while not authenticated:
        conn.send("Enter username:".encode("utf-8"))
        username = conn.recv(1024).decode("utf-8").strip()

        conn.send("Enter password:".encode("utf-8"))
        password = conn.recv(1024).decode("utf-8")

        success, message = login_user(username, password)
        if success:
            authenticated = True
            conn.send(message.encode("utf-8"))
        else:
            conn.send(message.encode("utf-8"))

    # Add the client to connected_clients once authenticated
    broadcaster.add_client(conn)
    broadcaster.broadcast(f"{username} has joined the chat!", conn)

    # Main chat loop
    connected = True
    while connected:
        try:
            msg = conn.recv(1024).decode("utf-8")
            if msg:
                print(f"{username} says: {msg}")
                broadcaster.broadcast(f"{username}: {msg}", conn)

                if msg == EXIT_COMMAND:
                    connected = False
        except:
            connected = False

    broadcaster.remove_client(conn)
    conn.close()
    broadcaster.broadcast(f"{username} has left the chat.", conn)
    print(f"Connection from {addr} closed")


if __name__ == "__main__":
    start()
