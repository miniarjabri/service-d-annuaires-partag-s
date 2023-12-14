import socket

def create_account(username, password):
    perform_action("create_account", username, password)

def login(username, password):
    perform_action("login", username, password)

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

    # Fermer la connexion
    client.close()

if __name__ == "__main__":
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
