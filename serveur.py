import socket

class Server:
    def __init__(self):
        # Adresse IP du serveur (localhost dans cet exemple)
        self.HOST = '127.0.0.1'
        # Port d'écoute du serveur
        self.PORT = 12345
        # Créer le Socket Serveur
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Lier le Socket à une Adresse et un Port
        self.server_socket.bind((self.HOST, self.PORT))
        # Écouter les Connexions Entrantes
        self.server_socket.listen()

    def start_server(self):
        print(f"Le serveur écoute sur le port {self.PORT}...")
        # Accepter les Connexions des Clients
        client_socket, client_address = self.server_socket.accept()
        print(f"Connexion établie avec {client_address}")

        # Gestion de la connexion
        while True:
            # Lire les données du client
            data = client_socket.recv(1024)
            if not data:
                break # La connexion a été interrompue

            # Traitez les données ici (à adapter selon vos besoins)
            print(f"Reçu du client ({client_address}): {data.decode('utf-8')}")

            response = "Message reçu par le serveur."
            client_socket.sendall(response.encode('utf-8'))

        client_socket.close()
        self.server_socket.close()

if __name__ == "__main__":
    server = Server()
    server.start_server()
