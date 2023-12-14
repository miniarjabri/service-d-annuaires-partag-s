import socket
import threading

# Dictionnaire pour stocker les informations d'authentification (à des fins de démonstration uniquement)
comptes = {}

def handle_client(client_socket):
    # Attendre les données du client
    request = client_socket.recv(1024).decode('utf-8')
    action, username, password = request.split(',')

    # Gérer l'action en fonction de la requête
    if action == "create_account":
        create_account(client_socket, username, password)
    elif action == "login":
        login(client_socket, username, password)
    else:
        response = "Action non reconnue."

        # Renvoyer la réponse au client
        client_socket.send(response.encode('utf-8'))
        client_socket.close()

def create_account(client_socket, username, password):
    # Vérifier si le compte existe déjà
    if username in comptes:
        response = "Le nom d'utilisateur existe déjà. Veuillez choisir un autre nom d'utilisateur."
    else:
        # Créer le compte
        comptes[username] = password
        response = "Compte créé avec succès."

    # Renvoyer la réponse au client
    client_socket.send(response.encode('utf-8'))
    client_socket.close()

def login(client_socket, username, password):
    # Vérifier si les informations d'identification sont correctes
    if username in comptes and comptes[username] == password:
        response = "Connexion réussie."
    else:
        response = "Échec de la connexion. Vérifiez vos informations d'identification."

    # Renvoyer la réponse au client
    client_socket.send(response.encode('utf-8'))
    client_socket.close()

def main():
    # Configuration du serveur
    host = '127.0.0.1'
    port = 12345

    # Création du socket du serveur
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)

    print(f"[*] Serveur en attente sur {host}:{port}")

    while True:
        # Accepter les connexions entrantes
        client, addr = server.accept()
        print(f"[*] Connexion acceptée de {addr[0]}:{addr[1]}")

        # Créer un thread pour gérer le client
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

if __name__ == "__main__":
    main()
