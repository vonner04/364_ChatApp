import socket
import threading

SERVER_IP = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 5555  # The same port number your server is listening on
EXIT_COMMAND = "!DISCONNECT"  # Command for client to disconnect


# Function to handle receiving messages from the server
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if message:
                print(message)
            else:
                break
        except:
            print("Connection lost to the server.")
            break


# Function to handle sending messages to the server
def send_messages(client_socket):
    while True:
        message = input()
        client_socket.send(message.encode("utf-8"))
        if message == EXIT_COMMAND:
            break


def main():
    # Connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((SERVER_IP, SERVER_PORT))
        print(f"Connected to server at {SERVER_IP}:{SERVER_PORT}")
    except Exception as e:
        print(f"Failed to connect to the server: {e}")
        return

    # Start a thread to handle receiving messages from the server
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    # Login process
    username = input()
    client_socket.send(username.strip().encode("utf-8"))

    password = input()
    client_socket.send(password.encode("utf-8"))

    # Wait for server response (login success or failure)
    response = client_socket.recv(1024).decode("utf-8")
    print(response)

    # If login is successful, enter the messaging loop

    # Wait for the receive thread to complete (in case the server disconnects first)
    receive_thread.join()

    # Close the socket when done
    client_socket.close()
    print("Disconnected from the server.")


if __name__ == "__main__":
    main()
