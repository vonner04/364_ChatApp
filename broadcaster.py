import socket


class Broadcaster:
    def __init__(self):
        self.connected_clients = []

    def add_client(self, client):
        self.connected_clients.append(client)

    def remove_client(self, client):
        if client in self.connected_clients:
            self.connected_clients.remove(client)

    def broadcast(self, message, sender_conn):
        for client in self.connected_clients:
            if client != sender_conn:
                client.send(message.encode("utf-8"))
