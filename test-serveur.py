#PORT = 56789
from serveur import Server

# Création d'une instance de la classe Server
server = Server()

# Test de la création de compte
created_account = server.create_account('utilisateur1', 'motdepasse1')

# Affichage du résultat du test
if created_account:
    print("Le compte a été créé avec succès!")
else:
    print("Échec de la création du compte. Nom d'utilisateur déjà pris.")