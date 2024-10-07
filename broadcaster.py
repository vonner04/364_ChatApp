class Broadcaster:
    def __init__(self):
        self.connected_clients = []
        self.client_usernames = {}

    def add_client(self, client_socket, username):
        self.connected_clients.append(client_socket)
        self.client_usernames[client_socket] = username

    def remove_client(self, client_socket):
        if client_socket in self.connected_clients:
            self.connected_clients.remove(client_socket)
        if client_socket in self.client_usernames:
            del self.client_usernames[client_socket]

    def broadcast(self, message, current_client):
        full_message = f"SERVER: {message}"

        for client in self.connected_clients:
            if client != current_client:
                try:
                    client.send(full_message.encode("utf-8"))
                except socket.error:
                    self.remove_client(client)
