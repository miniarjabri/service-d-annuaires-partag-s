import unittest
from serveur import Server

class TestServerFunctions(unittest.TestCase):
    def setUp(self):
        # Set up any necessary resources before each test
        self.server = Server()

    def tearDown(self):
        # Clean up any resources after each test
        self.server.server_socket.close()

    def test_create_account(self):
        # Test the create_account function
        response = self.server.create_account("test_user11", "test_password")
        self.assertEqual(response["status"], "success")

        # Test if the user already exists
        response_existing = self.server.create_account("user1", "pass123")
        self.assertEqual(response_existing["status"], "error")

    def test_login(self):
        print("début test_login")
        # Test the login function
        response = self.server.login("user1", "pass123")
        self.assertEqual(response["status"], "success")

        # Test with incorrect credentials
        response_incorrect = self.server.login("user1", "wrong_password")
        self.assertEqual(response_incorrect["status"], "error")

    def test_recherche_contact(self):
        # Test the recherche_contact function
        username = "user1"
        nom = "Nom"
        prenom = "Prenom"

        # Add a contact to the annuaire for testing
        annuaire_path = f"{username}_annuaire.txt"
        with open(annuaire_path, 'w') as annuaire_file:
            annuaire_file.write(f"{nom},{prenom},test@email.com,123456789\n")

        # Perform the recherche_contact
        response = self.server.recherche_contact(username, nom, prenom)

        # Check if the response is as expected
        expected_info = {"nom": nom, "prenom": prenom, "email": "test@email.com", "telephone": "123456789"}
        expected_response = {"status": "success", "client_info": expected_info}
        self.assertEqual(response, expected_response)

if __name__ == '__main__':
    unittest.main()