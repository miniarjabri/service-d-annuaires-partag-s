import socket
import json
import os
import threading
class Server:
    def __init__(self):
        self.HOST = '127.1.3.1'
        self.PORT = 1213
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.HOST, self.PORT))
        self.server_socket.listen()
        self.users_file = "utilisateurs.json"
        self.utilisateurs = self.load_users()
        self.connected_users = set()
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        print(f"Serveur en attente de connexions sur {self.HOST}:{self.PORT}...")
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Connexion établie avec {client_address}")
            self.handle_client(client_socket)
            # thread pour gérer chaque connexion
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()
    def handle_client(self, client_socket):
        print("Handling client connection...")
        try :
            while True:
                data = client_socket.recv(1024)
                if not data:
                    print("No data received from client.")
                    return

                decoded_data = data.decode('utf-8')
                request = json.loads(decoded_data)

                print(
                    f"Received login request for username: {request.get('username')}, password: {request.get('password')}")

                full_action = request.get('action')
                if isinstance(full_action, str):
                    print(f"Received action: {full_action}")

                    # Extract the actual action (without the dictionary structure)
                    action = request.get("action", "")
                    print(action)

                    if action == "create_account":
                        # Extract parameters from the "params" key
                        username, password = request.get("params", (None, None))

                        if username is not None and password is not None:
                            response = self.create_account(username, password)
                        else:
                            response = {"status": "error", "message": "Missing username or password in the request"}
                    elif action == "login":
                        # Extract parameters from the "params" key
                        username, password = request.get("params", (None, None))
                        if username is not None and password is not None:
                            response = self.login(username, password)
                        else:
                            response = {"status": "error", "message": "Missing username or password in the request"}
                        print("After login handling")

                    elif action == "ajouter_contact":
                        print("requete reçue")
                        # Extract parameters from the "params" key

                        username, nom,prenom,email,telephone = request.get("params", (None, None,None, None,None))

                        if username is not None and nom is not None  and prenom is not None  and email is not None  and telephone is not None:
                            response = self.ajouter_contact(username ,nom,prenom,email,telephone)
                        #else:
                        #response = self.ajouter_contact(request.get("username"), request.get("nom"),  request.get("prenom"), request.get("email"),      request.get("telephone"))
                    # Coté serveur
                    elif action == "recherche_contact":
                        print("Requête de recherche de client reçue")

                        # Extract parameters from the "params" key

                        username, nom, prenom= request.get("params", (None, None, None))

                        if username is not None and nom is not None and prenom is not None:
                            response = self.recherche_contact(username, nom, prenom)
                        else:
                            response = {"status": "error", "message": "Missing nom or prenom in the request"}
                    elif action == "afficher_contacts":
                        print("Requête d'affichage de tous les contacts reçue")

                        # Extract parameters from the "params" key
                        username = request.get("params", None)

                        if username is not None:
                            response = self.afficher_contacts(username)
                        else:
                            response = {"status": "error", "message": "Missing username in the request"}
                    elif action == "modifier_contact":
                        print("Requête de modification de contact reçue")

                        # Extract parameters from the "params" key
                        username, nom, prenom ,change, new_value = request.get("params", (None, None, None,None, None))

                        if username is not None and nom is not None and prenom is not None and change is not None and new_value is not None:
                            response = self.modifier_contact(username, nom,prenom,change,new_value)
                        else:
                            response = {"status": "error", "message": "Missing parameters in the request"}

                    elif action == "supprimer_contact":
                        print("Requête de modification de contact reçue")

                        # Extract parameters from the "params" key
                        username, nom, prenom  = request.get("params", (None, None, None))

                        if username is not None and nom is not None and prenom is not None:
                            response = self.supprimer_contact(username, nom,prenom)
                        else:
                            response = {"status": "error", "message": "Missing parameters in the request"}
                    elif action == "add_user":
                        new_username, new_password = request.get("params", (None, None))
                        if new_username is not None and new_password is not None:
                            response = self.add_user(new_username, new_password)
                        else:
                            response = {"status": "error", "message": "Missing username or password in the request"}




                    else:
                        response = {"status": "error", "message": "Invalid action"}
                else:
                    response = {"status": "error", "message": "Invalid action format in the request"}

                response_json = json.dumps(response)
                client_socket.send(response_json.encode('utf-8'))

        finally:
            client_socket.close()

    def save_users(self):
        try:
            with open(self.users_file, 'w') as users_file:
                json.dump(self.utilisateurs, users_file)
        except Exception as e:
            print(f"Error saving users: {e}")
    def create_account(self, username, password):
        try:
            print(f"Creating account for username: {username}, password: {password}")

            # Vérifier si le compte existe déjà
            if username in self.utilisateurs:
               return {"status": "error",
                    "message": "Le nom d'utilisateur existe déjà. Veuillez choisir un autre nom d'utilisateur."}

               # Créer le compte avec un annuaire vide
            annuaire_filename = f"{username}_annuaire.txt"
            with open( annuaire_filename, 'w') as user_file:
                user_file.write("Nom,Prénom,Email,Téléphone\n")

            self.utilisateurs[username] = {'password': password, 'annuaire': annuaire_filename}

            # Appeler une fonction de sauvegarde des utilisateurs (à implémenter correctement)
            self.save_users()

            return {"status": "success", "message": f"Compte {username} créé avec succès"}
        except Exception as e:
           print(f"Error in create_account: {e}")
           return {"status": "error", "message": "Erreur lors de la création du compte. Veuillez réessayer."}

    def load_users(self):
        try:
            with open(self.users_file, 'r') as users_file:
                return json.load(users_file)
        except FileNotFoundError:
            return {}

    def login(self, username, password):
        # Charger les utilisateurs depuis le fichier JSON
        #self.utilisateurs = self.load_users()
        print(f"Attempting login for username: {username}, password: {password}")
        print(f"Current utilisateurs data: {self.utilisateurs}")
        # Vérifier si les informations d'identification sont correctes
        if username in self.utilisateurs and self.utilisateurs[username]['password'] == password:
            return {"status": "success", "message": f"Connexion réussie en tant que {username}"}
        else:
            return {"status": "error", "message": "Nom d'utilisateur ou mot de passe incorrect"}

    # Ajoutez cette méthode dans la classe Server
    def ajouter_contact(self, username, nom, prenom, email, telephone):
        print("Début de la méthode ajouter_contact")

        # Charger les utilisateurs depuis le fichier JSON
        self.utilisateurs = self.load_users()

        # Vérifier si l'utilisateur est dans la liste des utilisateurs
        if username in self.utilisateurs:
            # Nom du fichier utilisateur
            filename = self.utilisateurs[username]['annuaire']
            print(f"Nom du fichier utilisateur: {filename}")
            # Lire les contacts actuels du fichier ou créer le fichier s'il n'existe pas
            try:
                with open(filename, 'r') as user_file:
                    lines = user_file.readlines()
            except FileNotFoundError:
                with open(filename, 'w') as user_file:
                    user_file.write("Nom,Prénom,Email,Téléphone\n")
                lines = []

            # Vérifier si le contact existe déjà
            contact_exists = any(f"{nom},{prenom},{email},{telephone}" in line for line in lines)
            print(f"Contact existe déjà: {contact_exists}")
            if not contact_exists:
                # Ajouter le contact à l'annuaire de l'utilisateur
                with open(filename, 'a') as user_file:
                    user_file.write(f"{nom},{prenom},{email},{telephone}\n")

                self.save_users()  # Sauvegarder les utilisateurs après la modification

                return {"status": "success", "message": "Contact ajouté avec succès."}
            else:
                return {"status": "error", "message": "Le contact existe déjà."}
        else:
            return {"status": "error", "message": "Vous n'êtes pas connecté."}


    def recherche_contact(self, username, nom, prenom):
        # Logique de recherche du client dans l'annuaire spécifique à l'utilisateur
        annuaire_path = f"{username}_annuaire.txt"

        try:
            with open(annuaire_path, 'r') as annuaire_file:
                for line in annuaire_file:
                    fields = line.strip().split(',')  # Supprime les espaces inutiles et divise la ligne en champs

                    if len(fields) >= 4 and fields[0] == nom and fields[1] == prenom:
                        nom_contact, prenom_contact, email, telephone = fields[:4]  # Ajoutez d'autres champs au besoin
                        client_info = {"nom": nom_contact, "prenom": prenom_contact, "email": email,
                                       "telephone": telephone}
                        response = {"status": "success", "client_info": client_info}
                        print(
                            f"Contact trouvé : {nom_contact} {prenom_contact}, Email: {email}, Téléphone: {telephone}")
                        break  # Arrête la recherche après avoir trouvé le contact
                else:
                    response = {"status": "error", "message": "Client not found in the annuaire"}

        except FileNotFoundError:
            response = {"status": "error", "message": "User annuaire not found"}
        return response

    def afficher_contacts(self, username):
        # Logique pour afficher tous les contacts de l'annuaire spécifique à l'utilisateur
        annuaire_path = f"{username}_annuaire.txt"
        print(f"Annuaire path: {annuaire_path}")

        try:
            with open(annuaire_path, 'r') as annuaire_file:
                all_contacts = []
                for line in annuaire_file:
                    fields = line.strip().split(',')  # Supprime les espaces inutiles et divise la ligne en champs

                    if len(fields) >= 4:
                        nom_contact, prenom_contact, email, telephone = fields[:4]  # Ajoutez d'autres champs au besoin
                        contact_info = {"nom": nom_contact, "prenom": prenom_contact, "email": email,
                                        "telephone": telephone}
                        all_contacts.append(contact_info)

                if all_contacts:
                    response = {"status": "success", "all_contacts": all_contacts}
                else:
                    response = {"status": "error", "message": "Aucun contact trouvé dans l'annuaire"}

        except FileNotFoundError:
            response = {"status": "error", "message": "User annuaire not found"}

        return response

    # ...

    def modifier_contact(self, username, nom, prenom, change, new_value):
        annuaire_path = f"{username}_annuaire.txt"
        lines = []

        try:
            # Read all lines from the annuaire file
            with open(annuaire_path, 'r') as annuaire_file:
                lines = annuaire_file.readlines()

            # Find the line corresponding to the contact
            contact_key = f"{nom},{prenom}"
            for i, line in enumerate(lines):
                fields = line.strip().split(',')
                if f"{fields[0]},{fields[1]}" == contact_key:
                    # Modify the specified field in the client's line
                    field_mapping = {"nom": 0, "prenom": 1, "email": 2, "telephone": 3}
                    field_index = field_mapping.get(change)

                    if field_index is not None:
                        fields[field_index] = new_value
                        # Update the line in the list of lines
                        lines[i] = ",".join(fields)

                        # Save the updated lines back to the annuaire file
                        with open(annuaire_path, 'w') as updated_file:
                            updated_file.writelines(lines)

                        response = {"status": "success", "message": "Contact modifié avec succès."}
                    else:
                        response = {"status": "error", "message": "Champ invalide à modifier."}

                    return response

            response = {"status": "error", "message": "Le contact n'existe pas dans votre annuaire."}
        except FileNotFoundError:
            response = {"status": "error", "message": "User annuaire not found."}

        return response

    # Ajouter cette méthode à votre classe Server
    def supprimer_contact(self, username, nom, prenom):
        annuaire_path = f"{username}_annuaire.txt"
        lines = []

        try:
            # Read all lines from the annuaire file
            with open(annuaire_path, 'r') as annuaire_file:
                lines = annuaire_file.readlines()

            # Find the line corresponding to the contact
            contact_key = f"{nom},{prenom}"
            for i, line in enumerate(lines):
                fields = line.strip().split(',')
                if f"{fields[0]},{fields[1]}" == contact_key:
                    # Remove the line from the list of lines
                    del lines[i]

                    # Save the updated lines back to the annuaire file
                    with open(annuaire_path, 'w') as updated_file:
                        updated_file.writelines(lines)

                    response = {"status": "success", "message": "Contact supprimé avec succès."}
                    return response

            response = {"status": "error", "message": "Le contact n'existe pas dans votre annuaire."}
        except FileNotFoundError:
            response = {"status": "error", "message": "User annuaire not found."}

        return response

    def add_user(self, new_username, new_password):
        # Charger les utilisateurs depuis le fichier JSON
        self.utilisateurs = self.load_users()

        # Vérifier si le nouvel utilisateur existe déjà
        if new_username in self.utilisateurs:
            return {"status": "error", "message": "Le client existe déjà."}
        else:
            try:
                if new_username == "rim" and new_password == "123":
                    return {"status": "error", "message": "Impossible de créer ce compte."}
                else:
                    # Créer le compte avec un annuaire vide
                    annuaire_filename = f"{new_username}_annuaire.txt"
                    with open(annuaire_filename, 'w') as annuaire_file:
                        annuaire_file.write("Nom,Prenom,Email,Telephone,Adresse postale, adresse mail\n")
                    self.utilisateurs[new_username] = {'password': new_password, 'annuaire': annuaire_filename}

                    print(f"Annuaire vide créé avec succès pour le nouvel utilisateur {new_username}.")

                    # Sauvegarder les utilisateurs dans le fichier JSON après l'ajout
                    self.save_users()

                    return {"status": "success", "message": f"Compte {new_username} créé avec succès."}
            except Exception as e:
                print(f"Error in add_user: {e}")
                return {"status": "error", "message": "Erreur lors de la création du compte. Veuillez réessayer."}

    def stop_server(self):
        self.server_socket.close()
        print("Server stopped.")

if __name__ == "__main__":
    server = Server()
    server.run()
    #server.stop_server()