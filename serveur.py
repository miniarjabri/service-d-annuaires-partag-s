import socket
import threading
import json
# Dictionnaire pour stocker les informations d'authentification et les annuaires
utilisateurs = {}
def save_connected_users():
    with open("connected_users.json", "w") as json_file:
        json.dump(list(connected_users), json_file)
def load_users():
    try:
        with open("utilisateurs.json", "r") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return {}
def handle_client(client_socket):
    # Attendre les données du client
    request = client_socket.recv(1024).decode('utf-8')

    # Initialiser action pour éviter UnboundLocalError
    action = None

    split_values = request.split(',')
    if len(split_values) == 3:
        action, username, password = split_values
    else:
        print("Erreur: La requête n'a pas le format attendu.")
        # Gérer l'erreur en envoyant une réponse au client
        response = "Erreur: La requête n'a pas le format attendu."
        client_socket.send(response.encode('utf-8'))
        client_socket.close()
        return

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

def create_user_file(username):
    # Create a user-specific file for contacts
    filename = f"{username}_annuaire.txt"
    with open(filename, 'w') as user_file:
        user_file.write("Nom,Prénom,Email,Téléphone\n")

def create_account(client_socket, username, password):
    global utilisateurs

    # Charger les utilisateurs depuis le fichier JSON
    utilisateurs = load_users()

    # Vérifier si l'utilisateur est dans la liste des utilisateurs
    if username in utilisateurs:
        response = "Le nom d'utilisateur existe déjà. Veuillez choisir un autre nom d'utilisateur."
    else:
        # Créer le compte avec un annuaire vide
        utilisateurs[username] = {'password': password, 'annuaire': {}}
        response = "Compte créé avec succès."

        # Créer le fichier utilisateur
        create_user_file(username)
    # Renvoyer la réponse au client
    client_socket.send(response.encode('utf-8'))
    client_socket.close()
    return response

def login(client_socket, username, password):
    global utilisateurs

    # Charger les utilisateurs depuis le fichier JSON
    utilisateurs = load_users()

    # Vérifier si l'utilisateur est dans la liste des utilisateurs
    if username in utilisateurs and utilisateurs[username]['password'] == password:
        connected_users.add(username)
        response = "Connexion réussie."
    else:
        response = "Échec de la connexion. Vérifiez vos informations d'identification."

    # Renvoyer la réponse au client
    client_socket.send(response.encode('utf-8'))
    client_socket.close()


def logout(client_socket, username):
    global utilisateurs

    # Charger les utilisateurs depuis le fichier JSON
    utilisateurs = load_users()

    # Vérifier si l'utilisateur est dans la liste des utilisateurs
    if username in utilisateurs:
        connected_users.remove(username)
        response = "Déconnexion réussie."
    else:
        response = "Vous n'êtes pas connecté."

    # Renvoyer la réponse au client
    client_socket.send(response.encode('utf-8'))
    client_socket.close()


def get_annuaire(client_socket, username):
    global utilisateurs

    # Charger les utilisateurs depuis le fichier JSON
    utilisateurs = load_users()

    # Vérifier si l'utilisateur est dans la liste des utilisateurs
    if username in utilisateurs:
        annuaire = utilisateurs[username]['annuaire']
        response = str(annuaire)
    else:
        response = "Vous n'êtes pas connecté."

    # Renvoyer la réponse au client
    client_socket.send(response.encode('utf-8'))
    client_socket.close()


def ajouter_contact(client_socket, username):
    global utilisateurs

    # Charger les utilisateurs depuis le fichier JSON
    utilisateurs = load_users()

    # Vérifier si l'utilisateur est dans la liste des utilisateurs
    if username in utilisateurs:
        nom, prenom, email, telephone = client_socket.recv(1024).decode('utf-8').split(',')

        # Vérifier si le contact existe déjà dans l'annuaire de l'utilisateur
        if nom not in utilisateurs[username]['annuaire']:
            # Ajouter le contact à l'annuaire de l'utilisateur
            utilisateurs[username]['annuaire'][nom] = {'prenom': prenom, 'email': email, 'telephone': telephone}

            # Ajouter le contact au fichier de l'utilisateur
            filename = f"{username}_annuaire.txt"
            with open(filename, 'a') as user_file:
                user_file.write(f"{nom},{prenom},{email},{telephone}\n")

            response = "Contact ajouté avec succès."
        else:
            response = "Le contact existe déjà dans votre annuaire."
    else:
        response = "Vous n'êtes pas connecté."

    # Renvoyer la réponse au client
    client_socket.send(response.encode('utf-8'))
    client_socket.close()


def supprimer_contact(client_socket, username):
    global utilisateurs

    # Charger les utilisateurs depuis le fichier JSON
    utilisateurs = load_users()

    # Vérifier si l'utilisateur est dans la liste des utilisateurs
    if username in utilisateurs:
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
    global utilisateurs

    # Charger les utilisateurs depuis le fichier JSON
    utilisateurs = load_users()

    # Vérifier si l'utilisateur est dans la liste des utilisateurs
    if username in utilisateurs:
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

    try:
        while True:
            # Accepter les connexions entrantes
            client, addr = server.accept()
            print(f"[*] Connexion acceptée de {addr[0]}:{addr[1]}")

            # Créer un thread pour gérer le client
            client_handler = threading.Thread(target=handle_client, args=(client,))
            client_handler.start()

    finally:
        # Sauvegarder la liste des utilisateurs connectés avant de fermer le serveur
        save_connected_users()
        server.close()

if __name__ == "__main__":
    connected_users = set()
    main()
