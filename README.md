# Partie Utilisateurs gérée par Miniar Jabri
au début le client reçoit ces 3 choix
1. Créer un compte
2. Se connecter
3. Quitter
   s'il choisit de créer un compte :

   coté client:
   
   on lui demande d'écrire le nom d'utilisateur et le mot de passe
   appel à la méthode create_account()
   dnas cette méthode , on envoie une requete "create_account" grace à la méthode "send_request"
   la méthode "send_request" envoie l'action et les autres parametres au serveur

   coté serveur:

   dans la méthode handle_client(), puisque l'action reçue de la part du client est "create_account", on envoie les autres parametres (username, password) à la méthode "create_account" pour créer le compte. cette méthode vérifie   
   
