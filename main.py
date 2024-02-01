import socket
import threading
from serveur import Serveur  # Supposons que le code du serveur est dans un fichier nommé Serveur.py

def send_request(sock, request):
    sock.send(request.encode('utf-8'))
    response = sock.recv(1024).decode('utf-8')
    print(response)

def main():
    # Création d'une instance de la classe Serveur
    server_instance = Serveur()

    # Configuration du serveur
    host = '127.0.0.1'
    port = '12345'

    # Création du socket client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    try:
        # Création de compte
        send_request(client, "create_account,user1,password1")

        # Connexion
        send_request(client, "login,user1,password1")

        # Ajout de contact
        send_request(client, "ajouter_contact,user1,John,Doe,john.doe@example.com,123456789")

        # Obtention de l'annuaire
        send_request(client, "get_annuaire,user1")

        # Déconnexion
        send_request(client, "logout,user1")

    finally:
        client.close()

if __name__ == "__main__":
    main()
