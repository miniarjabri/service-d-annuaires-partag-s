nom = input("Entrez le nom du contact que vous voulez modifier: ")
prenom = input("Entrez le prénom du contact que vous voulez modifier: ")
response = client.recherche_contact(username, nom, prenom)
if response["status"] == "success":
    print("Client found.")
    client.supprimer_contact(username,nom,prenom)
else:
    print("Client not found.")