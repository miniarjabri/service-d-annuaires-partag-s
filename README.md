# service-d-annuaires-partag-s
Nous souhaitons mettre en place un service d’annuaires partagés sur le modèle client/serveur pouvant fonctionner
en réseau. Le serveur de l’application stockera dans un ou plusieurs fichiers texte les données de ces annuaires
partagés. Il aura donc à gérer plusieurs annuaires. Chaque annuaire est associé à un utilisateur qui a un compte.
ATTENTION : Ne pas utiliser une base de données
Pour chaque contact dans l’annuaire, on stockera : le nom, le prénom, le numéro de téléphone portable, l’adresse
postale, l’adresse mail. Les champs nom, prénom et adresse mail sont obligatoires.
L’administrateur du serveur gèrera les comptes utilisateurs (création, suppression, modification…). A chaque
compte créé, un annuaire est créé et est associé à ce compte.
Un utilisateur (ayant un compte) peut, après connexion au serveur :
o gérer l’annuaire qu’il a créé (ajout, suppression, modification d’un contact…).
o consulter un autre annuaire si le propriétaire de l’annuaire lui a donné les permissions nécessaires.
Lors du lancement de l’entité (processus) cliente, un menu texte sera affiché pour permettre de choisir l’action à
réaliser. Tout d’abord, l’action de connexion (avec les paramètres d’authentification) et dès que la connexion est
réalisée, les actions de gestion selon le profil : administrateur du serveur ou utilisateur.
