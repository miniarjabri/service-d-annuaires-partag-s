import socket

HOST = '127.0.0.1'  # Adresse IP du serveur (localhost dans cet exemple)
PORT = 12345  # Port d'écoute du serveur

# Créez le Socket Client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connectez-vous au Serveur
client_socket.connect((HOST, PORT))

# Envoyez des données au serveur
message = "Hello, server!"
client_socket.sendall(message.encode('utf-8'))

# Recevez la réponse du serveur
data = client_socket.recv(1024)
print(f"Réponse du serveur: {data.decode('utf-8')}")

# Fermez la connexion
client_socket.close()
