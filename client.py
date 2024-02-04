import socket
import json

class Client:
    def __init__(self):
        self.HOST = '127.0.1.1'
        self.PORT = 1217
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.HOST, self.PORT))

    def send_request(self, action, *params):
        try:
            request_data = {"action": action, "params": params}
            # Convert sets to lists for serialization
            request_data["params"] = [list(param) if isinstance(param, set) else param for param in
                                      request_data["params"]]
            # Check if there's only one parameter and convert it to a list if needed
            if len(request_data["params"]) == 1:
                request_data["params"] = request_data["params"][0]
            request_json = json.dumps(request_data)
            self.client_socket.send(request_json.encode('utf-8'))

            response_data = self.client_socket.recv(1024)

            if not response_data:
                print("Empty response received")
                return

            response = json.loads(response_data.decode('utf-8'))
            print(response)
            return response

        except ConnectionAbortedError:
            print("Connection aborted by host")
            return None

    # Modifiez la méthode ajouter_contact dans la classe Client
    def ajouter_contact(self, username, nom, prenom, email, telephone):
        return self.send_request("ajouter_contact", username,nom,prenom,email,telephone)

    def create_account(self, username, password):
        return self.send_request("create_account", username, password)

    def login(self, username, password):
        print("Sending login request...")
        response = client.send_request("login", username, password)
        print("Received response:", response)
        return self.send_request("login", username, password)

    def close_connection(self):
        self.client_socket.close()

    def recherche_contact(self,username, nom, prenom):
         return self.send_request("recherche_contact",username, nom, prenom)

    def afficher_contacts(self,username):
       return self.send_request("afficher_contacts", username)

    def modifier_contact(self,username,nom,prenom,change,new_value):
       return self.send_request("modifier_contact", username,nom,prenom,change,new_value)

    # Ajouter cette méthode à votre classe Client
    def supprimer_contact(self, username, nom, prenom):
        return self.send_request("supprimer_contact", username, nom, prenom)


if __name__ == "__main__":
    client = Client()

    while True:
        print("1. Créer un compte")
        print("2. Se connecter")
        print("3. Quitter")

        choice = input("Choisissez une option : ")

        if choice == "1":
            username = input("Entrez le nom d'utilisateur : ")
            password = input("Entrez le mot de passe : ")
            create_account_response = client.create_account(username, password)
            print(create_account_response)

        elif choice == "2":
            username = input("Entrez le nom d'utilisateur : ")
            password = input("Entrez le mot de passe : ")
            try:
                login_response = client.login(username, password)
                # Le reste de votre code...

                if login_response and "status" in login_response and login_response["status"] == "success":
                    while True:
                        print(f"Bonjour, {username}!")
                        print("1. Ajouter un contact à l'annuaire")
                        print("2. Supprimer un contact de l'annuaire")
                        print("3. Modifier un contact de l'annuaire")
                        print("4.affichier mes contacts")
                        print("5.recherche d'un contact")
                        print("6. Se déconnecter")

                        choice = input("Choisissez une option : ")

                        if choice == "1":
                            nom = input("Entrez le nom du contact : ")
                            prenom = input("Entrez le prénom du contact : ")
                            email = input("Entrez l'email du contact : ")
                            telephone = input("Entrez le numéro de téléphone du contact : ")
                            client.ajouter_contact(username, nom, prenom, email, telephone)
                        elif choice == "2":
                            nom = input("Entrez le nom du contact que vous voulez modifier: ")
                            prenom = input("Entrez le prénom du contact que vous voulez modifier: ")
                            response = client.recherche_contact(username, nom, prenom)
                            if response["status"] == "success":
                                print("Client found.")
                                client.supprimer_contact(username,nom,prenom)
                            else:
                                print("Client not found.")

                        elif choice == "3":
                            nom = input("Entrez le nom du contact que vous voulez modifier: ")
                            prenom = input("Entrez le prénom du contact que vous voulez modifier: ")
                            response = client.recherche_contact(username, nom, prenom)
                            if response["status"] == "success":
                                print("Client found.")
                                # Prompt the client for the field to modify
                                print("Choisissez le champ que vous voulez modifier:")
                                print("1. Nom")
                                print("2. Prénom")
                                print("3. Email")
                                print("4. Téléphone")

                                choice = input("Entrez le numéro du champ que vous voulez modifier: ")
                                if choice == "1":
                                    change = "nom"
                                    new_value = input("donner le nouveau nom:")
                                    client.modifier_contact(username, nom, prenom, change, new_value)
                                elif choice == "2":
                                    change = "prenom"
                                    new_value = input("donner le nouveau prenom:")
                                    client.modifier_contact(username, nom, prenom, change, new_value)
                                elif choice == "3":
                                    change = "email"
                                    new_value = input("donner le nouveau mail")
                                    client.modifier_contact(username, nom, prenom, change, new_value)
                                elif choice == "4":
                                    change = "telephone"
                                    new_value = input("donner le nouveau telephone:")
                                    client.modifier_contact(username, nom, prenom, change, new_value)
                                else:
                                    print("Choix invalide.")

                            else:
                                print("Client not found.")


                        # modifier_contact(username)
                        elif choice == "4":
                          client.afficher_contacts(username)

                        elif choice == "5":
                            nom = input("Entrez le nom du contact que vous cherchez : ")
                            prenom = input("Entrez le prénom du contact que vous cherchez : ")
                            client.recherche_contact(username,nom,prenom)

                        elif choice == "6":
                            break
                        else:
                            print("Option non valide. Veuillez réessayer.")


                else:
                    print(f"Échec de la connexion : {login_response.get('message', 'Erreur inconnue')}")

            except Exception as e:
                    print(f"Erreur lors de la connexion : {e}")

        elif choice == "3":
            break
        else:
            print("Option non valide. Veuillez réessayer.")

  # Exemple d'une action non valide
    # invalid_action_response = client.send_request("invalid_action", "user1", "pass123")
    # print(invalid_action_response)

   # client.client_socket.close()