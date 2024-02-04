# Partie Utilisateurs gérée par Miniar Jabri
au début le client reçoit ces 3 choix
1. Créer un compte
2. Se connecter
3. Quitter
   
   s'il choisit de créer un compte :

   coté client:
   
   on lui demande d'écrire le nom d'utilisateur et le mot de passe
   appel à la méthode create_account()
   dans cette méthode , on envoie une requete "create_account" grace à la méthode "send_request"
   la méthode "send_request" envoie l'action et les autres parametres au serveur

   coté serveur:

   dans la méthode handle_client(), puisque l'action reçue de la part du client est "create_account", on envoie les autres parametres (username, password) à la méthode "create_account" pour créer le compte. cette méthode vérifie si le 'username' n'exite pas dans le fichier utilisateurs.json, s'il exite elle affiche "Le nom d'utilisateur existe déjà. Veuillez choisir un autre nom d'utilisateur." sinon le compte sera crée un annuaire associé à ce nouveau compte sera crée et stocke dans le fichier utilisateurs.json : le username, le password, et le nom de l'annuaire du client.
   on aura dans le fichier utilisateur.json par exemple: "rim": {"password": "123", "annuaire": "rim_annuaire.txt"}
   
   le client recevra cette reponse du serveur

   s'il choisit de se connecter :

   coté client:
   
   on lui demande d'écrire le nom d'utilisateur et le mot de passe
   appel à la méthode login()
   dans cette méthode , on envoie une requete "login" grace à la méthode "send_request" 
   la méthode "send_request" envoie l'action et les autres parametres au serveur

   coté serveur:

   dans la méthode handle_client(), puisque l'action reçue de la part du client est "login", on envoie les autres parametres (username, password) à la méthode "login" de la classe serveur pour se connecter. cette méthode vérifie si le 'username' exite dans le fichier utilisateurs.json, s'il exite elle affiche "connexion reussie." sinon elle affiche "Nom d'utilisateur ou mot de passe incorrect"

   
   le client recevra cette reponse du serveur


     si aprés avoir connecter, le client choisit de cherche un contact dans son annuaire:

   coté client:
   
   on lui demande d'écrire le nom et le prenom du contact qu'il cherche
   appel à la méthode recherche_contact() de la classe client
   dans cette méthode , on envoie une requete "recherche_contact" grace à la méthode "send_request" 
   la méthode "send_request" envoie l'action "recherche_contact" et les autres parametres au serveur
   

   coté serveur:

   dans la méthode handle_client(), puisque l'action reçue de la part du client est recherche_contact", on envoie les autres parametres (username, nom, prenom) à la méthode "recherche_contact" de la classe serveur. cette méthode vérifie si le nom et le prenom existent dans l'annuaire du client, s'il exite elle affiche tous ses coordonnées (nom,prenom,email,telephone) sinon elle affiche "Client not found in the annuaire"
   le client recevra cette reponse du serveur
   
   

      
