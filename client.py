import socket
import os
import json


def save_users(utilisateurs):
    with open("utilisateurs.json", "w") as json_file:
        json.dump(utilisateurs, json_file)


def load_users():
    try:
        with open("utilisateurs.json", "r") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return {}





def login(username, password, is_admin=False):
    global utilisateurs

    # Charger les utilisateurs depuis le fichier JSON
    utilisateurs = load_users()

    # Vérifier si les informations d'identification sont correctes
    if username=="rim" and password=="123":
        connected_admin_menu(username)
    elif username in utilisateurs and utilisateurs[username]['password'] == password:

        connected_menu(username)
    else:
        print("username non trouvé veuillez réessayer")

    return perform_action("login", username, password)


def connected_menu(username):
    while True:
        print(f"Bonjour, {username}!")
        print("1. Ajouter un contact à l'annuaire")
        print("2. Supprimer un contact de l'annuaire")
        print("3. Modifier un contact de l'annuaire")
        print("4.affichier mes contacts")
        print("5. Se déconnecter")

        choice = input("Choisissez une option : ")

        if choice == "1":
            ajouter_contact(username)
        elif choice == "2":
            supprimer_contact(username)
        elif choice == "3":
            modifier_contact(username)
        elif choice == "4":
            get_annuaire(username)
        elif choice == "5":
            logout(username)
            return
        else:
            print("Option non valide. Veuillez réessayer.")


def connected_admin_menu(admin_username):
    while True:
        print(f"Bonjour, administrateur {admin_username}!")
        print("1. Gérer les utilisateurs")
        print("2. Se déconnecter")

        choice = input("Choisissez une option : ")

        if choice == "1":
            manage_users()

        elif choice == "2":
            logout(admin_username)
            return
        else:
            print("Option non valide. Veuillez réessayer.")


def manage_users():
    print("1. Ajouter un utilisateur")
    print("2. Supprimer un utilisateur")
    print("3. Modifier un utilisateur")
    print("4. Lister des utilisateurs")
    print("5. Retour au menu principal")

    user_choice = input("Choisissez une option : ")

    if user_choice == "1":
        add_user()
    elif user_choice == "2":
        delete_user()
    elif user_choice == "3":
        modify_user()
    elif user_choice == "4":
        list_users()
    elif user_choice == "5":
        return
    else:
        print("Option non valide. Veuillez réessayer.")


# -------------------------------------------------
def add_user():
    global utilisateurs

    # Charger les utilisateurs depuis le fichier JSON
    utilisateurs = load_users()

    new_username = input("Entrez le nom d'utilisateur pour le nouvel utilisateur : ")
    new_password = input("Entrez le mot de passe pour le nouvel utilisateur : ")

    # Vérifier si le nouvel utilisateur existe déjà
    if new_username not in utilisateurs:
        if (new_username == "rim" and new_password == "123"):
            print("impossible de créer ce compte")
        # Créer le compte avec un annuaire vide
        else:
            annuaire_filename = f"{new_username}_annuaire.txt"
            utilisateurs[new_username] = {'password': new_password, 'annuaire': annuaire_filename}

            print("Utilisateur ajouté avec succès.")

            # Créer un annuaire vide pour le nouvel utilisateur
            annuaire_filename = f"{new_username}_annuaire.txt"
            with open(annuaire_filename, 'w') as annuaire_file:
                annuaire_file.write("Nom,Prenom,Email,Telephone,Adresse postale, adresse mail\n")

            print("Annuaire vide créé avec succès pour le nouvel utilisateur.")

            # Sauvegarder les utilisateurs dans le fichier JSON après l'ajout
            with open("utilisateurs.json", "a") as json_file:
                json.dump(utilisateurs, json_file)
            save_users(utilisateurs)
    else:
        print("l'utilisateur existe déja")



# ----------------------------------------
def create_user_file(new_username):
    # Créer un annuaire vide pour le nouvel utilisateur
    annuaire_filename = f"{new_username}_annuaire.txt"
    with open(annuaire_filename, 'w') as annuaire_file:
        annuaire_file.write("Nom,Prenom,Email,Telephone,Adresse postale, adresse mail\n")


# -------------------
def delete_user():
    global utilisateurs
    global server

    # Charger les utilisateurs depuis le fichier JSON
    utilisateurs = load_users()

    print("Liste des utilisateurs :")
    for i, username in enumerate(utilisateurs, start=1):
        print(f"{i}. {username}")

    if not utilisateurs:
        print("Aucun utilisateur à supprimer.")
        return

    try:
        user_index = int(input("Entrez le numéro de l'utilisateur à supprimer : "))
        if 1 <= user_index <= len(utilisateurs):
            # Obtenir le nom d'utilisateur à supprimer
            username = list(utilisateurs.keys())[user_index - 1]
            #-------------------------------------------------

            if username in utilisateurs:


                annuaire_filename = f"{username}_annuaire.txt"
                print(annuaire_filename)
                try:
                    # Vérifier si le fichier existe avant de tenter de le supprimer
                    if os.path.exists(annuaire_filename):
                        print(os.path)
                        os.remove(annuaire_filename)
                except Exception as e:
                    # Gérer toute exception lors de la suppression du fichier
                    print(f"Erreur lors de la suppression du fichier : {e}")

                response = f"L'utilisateur '{username}' a été supprimé avec succès."
            else:
                response = "L'utilisateur n'existe pas."
            #---------------------------------------

            # Supprimer l'utilisateur
            del utilisateurs[username]


            # Mettre à jour le fichier JSON
            save_users(utilisateurs)


            print(f"L'utilisateur '{username}' a été supprimé avec succès.")
        else:
            print("Numéro d'utilisateur invalide.")
    except ValueError:
        print("Veuillez entrer un numéro valide.")


# ----------------------------------------------------------------


# Création du socket du client


# Envoi des données au serveur


# Recevoir la réponse du serveur



# ----------------------------------------------------------------
def modify_user():
    global utilisateurs

    # Charger les utilisateurs depuis le fichier JSON
    utilisateurs = load_users()

    username_to_modify = input("Entrez le nom d'utilisateur à modifier : ")

    # Vérifier si l'utilisateur à modifier existe
    if username_to_modify in utilisateurs:
        print(f"Choisissez les informations à modifier pour l'utilisateur '{username_to_modify}' :")
        print("1. Mot de passe")
        print("2. Nom d'utilisateur")
        print("3. Annuler")

        choice = input("Choisissez une option : ")

        if choice == "1":
            new_password = input("Entrez le nouveau mot de passe : ")
            utilisateurs[username_to_modify]['password'] = new_password
            print(f"Mot de passe de l'utilisateur '{username_to_modify}' modifié avec succès.")
        elif choice == "2":
            new_username = input("Entrez le nouveau nom d'utilisateur : ")

            # Demander confirmation à l'administrateur
            confirm = input(
                f"Voulez-vous vraiment changer le nom d'utilisateur de '{username_to_modify}' à '{new_username}'? (O/N) : ")

            if confirm.upper() == "O":
                # Modifier le nom d'utilisateur
                utilisateurs[new_username] = utilisateurs.pop(username_to_modify)
                print(f"Nom d'utilisateur de '{username_to_modify}' modifié avec succès.")
            else:
                print("Modification annulée.")
        elif choice == "3":
            print("Modification annulée.")
        else:
            print("Option non valide.")

        # Mettre à jour le fichier JSON
        save_users(utilisateurs)

    else:
        print(f"L'utilisateur '{username_to_modify}' n'existe pas.")


def list_users():
    global utilisateurs
    print("Liste des utilisateurs :")
    for username in utilisateurs:
        print(username)
    print()


def create_user_directory():
    username_to_create_directory = input("Entrez le nom d'utilisateur pour créer un annuaire : ")
    # Ajoutez la logique pour créer un annuaire pour l'utilisateur spécifié.


# -------------------------------------

def logout(username):
    perform_action("logout", username, "")


def get_annuaire(username):
    perform_action("get_annuaire", username, "")


def ajouter_contact(username):
    global utilisateurs

    # Charger les utilisateurs depuis le fichier JSON
    utilisateurs = load_users()

    # Vérifier si l'utilisateur est dans la liste des utilisateurs
    if username in utilisateurs:

        # Nom du fichier utilisateur
        filename = f"{username}_annuaire.txt"

        nom = input("Entrez le nom du contact : ")
        prenom = input("Entrez le prénom du contact : ")
        email = input("Entrez l'email du contact : ")
        telephone = input("Entrez le numéro de téléphone du contact : ")

        # Ajouter le contact à l'annuaire de l'utilisateur
        utilisateurs[username]['annuaire'][nom] = {'prenom': prenom, 'email': email, 'telephone': telephone}

        # Ajouter le contact au fichier de l'utilisateur
        with open(filename, 'a') as user_file:
            user_file.write(f"{nom},{prenom},{email},{telephone}\n")

        print("Contact ajouté avec succès.")

    else:
        print("Vous n'êtes pas connecté.")

def supprimer_contact(username):
    global utilisateurs

    # Vérifier si l'utilisateur est connecté
    if username in utilisateurs:  # Nom du fichier utilisateur
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
    global utilisateurs

    # Vérifier si l'utilisateur est connecté
    if username in utilisateurs:
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

    if action == "logout":
        main()
    # Fermer la connexion
    client.close()
    # return response


def main():


    host='127.0.0.1'
    port=12345
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((host,port))



    while True:

        print("1. Se connecter")
        print("2. Quitter")

        choice = input("Choisissez une option : ")



        if choice == "1":
            print("Choisissez le type de connexion :")
            print("1. Se connecter en tant qu'administrateur")
            print("2. Se connecter en tant qu'utilisateur")

            connection_type = input("Choisissez une option : ")

            if connection_type == "1":
                # Connexion en tant qu'administrateur
                username = input("Entrez le nom d'utilisateur administrateur : ")
                password = input("Entrez le mot de passe administrateur : ")
                is_admin = True
            elif connection_type == "2":
                # Connexion en tant qu'utilisateur
                username = input("Entrez le nom d'utilisateur : ")
                password = input("Entrez le mot de passe : ")
                is_admin = False
            else:
                print("Option non valide. Veuillez réessayer.")
                continue

            response = login(username, password, is_admin)

            if response:
                connected_menu(username)
            else:
                print(response)
        elif choice == "2":

            return None

        else:

            print("Option non valide. Veuillez réessayer.")


if __name__ == "__main__":
    main()
