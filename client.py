import socket
import os
def create_account(username, password):
    return perform_action("create_account", username, password)


def login(username, password):
    if username in connected_users:
        connected_menu(username)
    return perform_action("login", username, password)


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
    # Nom du fichier utilisateur
    filename = f"{username}_annuaire.txt"

    # Vérifier si le fichier utilisateur existe
    if not os.path.isfile(filename):
        print("Vous n'êtes pas connecté.")
        perform_action("ajouter_contact", username, "")
        return

    nom = input("Entrez le nom du contact : ")
    prenom = input("Entrez le prénom du contact : ")
    email = input("Entrez l'email du contact : ")
    telephone = input("Entrez le numéro de téléphone du contact : ")

    # Lire les contacts actuels du fichier
    with open(filename, 'r') as user_file:
        lines = user_file.readlines()

    # Vérifier si le contact existe déjà
    contact_exists = any(f"{nom},{prenom},{email},{telephone}" in line for line in lines)

    if not contact_exists:
        # Ajouter le contact à l'annuaire de l'utilisateur
        with open(filename, 'a') as user_file:
            user_file.write(f"{nom},{prenom},{email},{telephone}\n")

        print("Contact ajouté avec succès.")
        connected_menu(username)
    else:
        print("Le contact existe déjà.")
        connected_menu(username)

    perform_action("ajouter_contact", username, "")

def supprimer_contact(username):
    # Vérifier si l'utilisateur est connecté
    if username in connected_users:
        # Nom du fichier utilisateur
        filename = f"{username}_annuaire.txt"

        # Lire les contacts actuels du fichier
        with open(filename, 'r') as user_file:
            lines = user_file.readlines()

        if not lines or len(lines) == 1:
            print("Aucun contact à supprimer.")
            return

        # Afficher les contacts actuels pour que l'utilisateur puisse choisir
        print("Contacts actuels:")
        for i, line in enumerate(lines[1:], start=1):
            print(f"{i}. {line.strip()}")

        # Demander à l'utilisateur de choisir le contact à supprimer
        try:
            index_to_remove = int(input("Entrez le numéro du contact à supprimer : "))
            if 1 <= index_to_remove <= len(lines) - 1:
                # Supprimer le contact choisi
                removed_contact = lines.pop(index_to_remove)
                print(f"Contact supprimé : {removed_contact.strip()}")

                # Réécrire les contacts dans le fichier
                with open(filename, 'w') as user_file:
                    user_file.write(lines[0])  # Écrire l'en-tête
                    user_file.writelines(lines[1:])
            else:
                print("Numéro de contact invalide.")
        except ValueError:
            print("Veuillez entrer un numéro valide.")
    else:
        print("Vous n'êtes pas connecté.")

def modifier_contact(username):
        # Vérifier si l'utilisateur est connecté
        if username in connected_users:
            # Nom du fichier utilisateur
            filename = f"{username}_annuaire.txt"

            # Lire les contacts actuels du fichier
            with open(filename, 'r') as user_file:
                lines = user_file.readlines()

            if not lines or len(lines) == 1:
                print("Aucun contact à modifier.")
                return

            # Afficher les contacts actuels pour que l'utilisateur puisse choisir
            print("Contacts actuels:")
            for i, line in enumerate(lines[1:], start=1):
                print(f"{i}. {line.strip()}")

            # Demander à l'utilisateur de choisir le contact à modifier
            try:
                index_to_modify = int(input("Entrez le numéro du contact à modifier : "))
                if 1 <= index_to_modify <= len(lines) - 1:
                    # Récupérer les détails du contact à modifier
                    contact_details = lines[index_to_modify].strip().split(',')

                    # Afficher les détails actuels du contact
                    print("Détails actuels du contact:")
                    print(f"1. Nom: {contact_details[0]}")
                    print(f"2. Prénom: {contact_details[1]}")
                    print(f"3. Email: {contact_details[2]}")
                    print(f"4. Téléphone: {contact_details[3]}")

                    # Demander à l'utilisateur de choisir le champ à modifier
                    field_to_modify = int(input("Entrez le numéro du champ à modifier : "))

                    # Demander à l'utilisateur de saisir la nouvelle valeur
                    new_value = input("Entrez la nouvelle valeur : ")

                    # Modifier le champ choisi
                    contact_details[field_to_modify - 1] = new_value

                    # Mettre à jour la ligne dans la liste des contacts
                    lines[index_to_modify] = ','.join(contact_details) + '\n'

                    print("Contact modifié avec succès.")

                    # Réécrire les contacts dans le fichier
                    with open(filename, 'w') as user_file:
                        user_file.write(lines[0])  # Écrire l'en-tête
                        user_file.writelines(lines[1:])
                else:
                    print("Numéro de contact invalide.")
            except ValueError:
                print("Veuillez entrer un numéro valide.")
        else:
            print("Vous n'êtes pas connecté.")


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
    return response

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
            response = create_account(username, password)
            if "Compte créé avec succès" in response.lower():
                connected_users.add(username)
            else:
                print(response)

        elif choice == "2":
            username = input("Entrez le nom d'utilisateur : ")
            password = input("Entrez le mot de passe : ")
            response = login(username, password)
            if "Connexion réussie" in response:
                connected_users.add(username)
                connected_menu(username)
            else:
                print(response)
        elif choice == "3":
            break
        else:
            print("Option non valide. Veuillez réessayer.")
