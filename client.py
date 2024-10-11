import socket
import threading
import sys 

SERVER_IP = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 5555


# Function to receive messages from the server
def receive_messages(client_socket):
    while True:
        try:
            # Receive and print messages from the server
            message = client_socket.recv(1024).decode("utf-8")
            sys.stdout.write(f"{message}\n")
            sys.stdout.flush()
            
        except:
            print("Connection lost...")
            client_socket.close()
            break


# Function to send messages to the server
def send_messages(client_socket):
    while True:
        # Send input from the user to the server
        message = input("")
        client_socket.send(message.encode("utf-8"))


def start_client():
    # Establish connection to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))

    # Start a thread to receive messages from the server
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    # Start a thread to send messages to the server
    send_thread = threading.Thread(target=send_messages, args=(client_socket,))
    send_thread.start()


if __name__ == "__main__":
    start_client()
