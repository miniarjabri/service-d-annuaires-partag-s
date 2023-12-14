import socket

def create_account(username, password):
    perform_action("create_account", username, password)

def login(username, password):
    perform_action("login", username, password)
    if username in connected_users:
        connected_menu(username)



def connected_menu(username):
    while True:
        print(f"Bonjour, {username}!")
        print("1. Ajouter un contact à l'annuaire")
        print("2. Supprimer un contact de l'annuaire")
        print("3. Modifier un contact de l'annuaire")
        print("4. Se déconnecter")

        choice = input("Choisissez une option : ")

        if choice == "1":
            ajouter_contact(username)
        elif choice == "2":
            supprimer_contact(username)
        elif choice == "3":
            modifier_contact(username)
        elif choice == "4":
            logout(username)
            break
        else:
            print("Option non valide. Veuillez réessayer.")

def logout(username):
    perform_action("logout", username, "")

def get_annuaire(username):
    perform_action("get_annuaire", username, "")

def ajouter_contact(username):
    perform_action("ajouter_contact", username, "")

def supprimer_contact(username):
    perform_action("supprimer_contact", username, "")

def modifier_contact(username):
    perform_action("modifier_contact", username, "")

def perform_action(action, username, password):
    # Configuration du client
    host = '127.0.0.1'
    port = 12345

    # Création du socket du client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    # Envoi des données au serveur
    data = f"{action},{username},{password}"
    client.send(data.encode('utf-8'))

    # Recevoir la réponse du serveur
    response = client.recv(1024).decode('utf-8')
    print(f"[*] Réponse du serveur : {response}")

    # Si l'action est de récupérer l'annuaire, imprimer l'annuaire
    if action == "get_annuaire":
        print(f"Votre annuaire : {response}")

    # Fermer la connexion
    client.close()

if __name__ == "__main__":
    connected_users = set()

    while True:
        print("1. Créer un compte")
        print("2. Se connecter")
        print("3. Quitter")

        choice = input("Choisissez une option : ")

        if choice == "1":
            username = input("Entrez le nom d'utilisateur : ")
            password = input("Entrez le mot de passe : ")
            create_account(username, password)
        elif choice == "2":
            username = input("Entrez le nom d'utilisateur : ")
            password = input("Entrez le mot de passe : ")
            login(username, password)
        elif choice == "3":
            break
        else:
            print("Option non valide. Veuillez réessayer.")
