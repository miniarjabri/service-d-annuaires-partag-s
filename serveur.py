import socket
import threading

# Dictionnaire pour stocker les informations d'authentification et les annuaires
utilisateurs = {}


def handle_client(client_socket):
    # Attendre les données du client
    request = client_socket.recv(1024).decode('utf-8')
    action, username, password = request.split(',')

    # Gérer l'action en fonction de la requête
    if action == "create_account":
        create_account(client_socket, username, password)
    elif action == "login":
        login(client_socket, username, password)
    elif action == "get_annuaire":
        get_annuaire(client_socket, username)
    elif action == "ajouter_contact":
        ajouter_contact(client_socket, username)
    elif action == "supprimer_contact":
        supprimer_contact(client_socket, username)
    elif action == "modifier_contact":
        modifier_contact(client_socket, username)
    elif action == "logout":
        logout(client_socket, username)
    else:
        response = "Action non reconnue."

        # Renvoyer la réponse au client
        client_socket.send(response.encode('utf-8'))
        client_socket.close()


def create_account(client_socket, username, password):
    # Vérifier si le compte existe déjà
    if username in utilisateurs:
        response = "Le nom d'utilisateur existe déjà. Veuillez choisir un autre nom d'utilisateur."
    else:
        # Créer le compte avec un annuaire vide
        utilisateurs[username] = {'password': password, 'annuaire': {}}
        response = "Compte créé avec succès."

    # Renvoyer la réponse au client
    client_socket.send(response.encode('utf-8'))
    client_socket.close()


def login(client_socket, username, password):
    # Vérifier si les informations d'identification sont correctes
    if username in utilisateurs and utilisateurs[username]['password'] == password:
        connected_users.add(username)
        response = "Connexion réussie."
    else:
        response = "Échec de la connexion. Vérifiez vos informations d'identification."

    # Renvoyer la réponse au client
    client_socket.send(response.encode('utf-8'))
    client_socket.close()


def logout(client_socket, username):
    # Vérifier si l'utilisateur est connecté
    if username in connected_users:
        connected_users.remove(username)
        response = "Déconnexion réussie."
    else:
        response = "Vous n'êtes pas connecté."

    # Renvoyer la réponse au client
    client_socket.send(response.encode('utf-8'))
    client_socket.close()


def get_annuaire(client_socket, username):
    # Vérifier si l'utilisateur est connecté
    if username in connected_users:
        annuaire = utilisateurs[username]['annuaire']
        response = str(annuaire)
    else:
        response = "Vous n'êtes pas connecté."

    # Renvoyer la réponse au client
    client_socket.send(response.encode('utf-8'))
    client_socket.close()


def ajouter_contact(client_socket, username):
    # Vérifier si l'utilisateur est connecté
    if username in connected_users:
        nom, prenom, email, telephone = client_socket.recv(1024).decode('utf-8').split(',')

        # Ajouter le contact à l'annuaire de l'utilisateur
        utilisateurs[username]['annuaire'][nom] = {'prenom': prenom, 'email': email, 'telephone': telephone}
        response = "Contact ajouté avec succès."
    else:
        response = "Vous n'êtes pas connecté."

    # Renvoyer la réponse au client
    client_socket.send(response.encode('utf-8'))
    client_socket.close()


def supprimer_contact(client_socket, username):
    # Vérifier si l'utilisateur est connecté
    if username in connected_users:
        nom = client_socket.recv(1024).decode('utf-8')

        # Supprimer le contact de l'annuaire de l'utilisateur
        if nom in utilisateurs[username]['annuaire']:
            del utilisateurs[username]['annuaire'][nom]
            response = "Contact supprimé avec succès."
        else:
            response = "Le contact n'existe pas dans votre annuaire."
    else:
        response = "Vous n'êtes pas connecté."

    # Renvoyer la réponse au client
    client_socket.send(response.encode('utf-8'))
    client_socket.close()


def modifier_contact(client_socket, username):
    # Vérifier si l'utilisateur est connecté
    if username in connected_users:
        nom, nouveau_prenom, nouveau_email, nouveau_telephone = client_socket.recv(1024).decode('utf-8').split(',')

        # Vérifier si le contact existe
        if nom in utilisateurs[username]['annuaire']:
            # Modifier le contact dans l'annuaire de l'utilisateur
            utilisateurs[username]['annuaire'][nom] = {
                'prenom': nouveau_prenom,
                'email': nouveau_email,
                'telephone': nouveau_telephone
            }
            response = "Contact modifié avec succès."
        else:
            response = "Le contact n'existe pas dans votre annuaire."
    else:
        response = "Vous n'êtes pas connecté."

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
    connected_users = set()
    main()
