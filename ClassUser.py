# from ClassDataBase import DataBase
from random import randint


class User:
    """
    Class allowing the user to interact with the database from the command line
    """

    def __init__(self, dataBase):
        # Class constructor
        self.dataBase = dataBase

    def reset_database(self):
        menu1 = True
        while menu1:
            try:
                choix_user = int(
                    input(
                        f"\n Bonjour et bienvenue. Veuillez entrer votre choix en sélectionnant un numéro :\n"
                        f"\n 1- Réinitialiser la base de données \n"
                        f"\n 2- Utiliser directement le programme\n"
                    )
                )
                if choix_user == 1:
                    print("Voici votre choix:\n")
                    self.dataBase.set_database()
                    self.dataBase.set_tables()
                    self.dataBase.set_product()
                    self.dataBase.set_category()
                    self.dataBase.set_categorized()
                    self.run()
                    break
                elif choix_user == 2:
                    print(f"\n Que souhaitez-vous faire? Sélectionnez un numéro :\n")
                    self.run()
                    break
            except ValueError:
                print("Veuillez préciser votre choix, entrez 1 ou 2")

    def menu_category(self):
        """
        Function used to display the list of categories by calling the get_category() method
        """
        print(f"\n Voici les catégories que nous vous proposons :\n")
        categories = self.dataBase.get_category()
        for i in range(len(categories)):
            print(f"{i+1} - {categories[i][1]}")
        menu_category = True
        while menu_category:
            # display the menu_category and ask the user to make a choice among a list of categories
            try:
                choix_category = int(
                    input("Sélectionner un numéro de catégorie entre 1 et 5 \n")
                )
                if choix_category > 0 <= (len(categories)):
                    self.menu_product(categories[choix_category - 1][0])
                    menu_category = False
                    print(f"\n Voulez-vous continuer? Sélectionnez un numéro :\n")
            except ValueError:
                print("Vous n'avez pas choisi de nombre entre 1 et 5")
                choix_category = int(
                    input("Sélectionner un numéro de catégorie entre 1 et 5 \n")
                )

    def menu_product(self, id_category):
        """
        Function used to display the list of products by calling the get_product() method
        """
        print(f"\n Voici les produits que nous avons trouvées pour cette catégorie :\n")
        products = self.dataBase.get_product(id_category)
        for i in range(len(products)):
            print(f"{i+1} - {products[i][1]}")
        # menu_product loop.
        menu_product = True
        while menu_product:
            # display the menu_product and ask the user to select a product among those displayed
            try:
                choix_product = int(
                    input("Sélectionnez un produit en entrant un numéro entre 1 et 5\n")
                )
                print(f"\n Voici les détails du produit que vous avez choisi:\n")
                # Display of products with their parameters
                print(f" - id: {products[choix_product-1][0]}")
                print(f" - nom: {products[choix_product-1][1]}")
                print(f" - magasin : {products[choix_product-1][2]}")
                print(f" - url: {products[choix_product-1][3]}")
                print(f" - code: {products[choix_product-1][4]}")
                print(f" - nutriscore: {products[choix_product-1][5]}")

                if choix_product > 0 <= (len(products)):
                    # Calling up the substitut menu
                    self.menu_substitut(
                        products[choix_product - 1][0],
                        id_category,
                        products[choix_product - 1][5],
                    )
                menu_product = False
            except ValueError:
                print("Vous n'avez pas sélectionné de produit")
                choix_product = int(input("Sélectionnez un produit"))

    def menu_substitut(self, id_product, id_category, nutriscore):
        """
        Function used to display the list of products by calling the get_substitut() method
        """
        print("test")
        substituts = self.dataBase.get_substitut(id_product, id_category, nutriscore)

        try:
            rand = randint(0, len(substituts) - 1)
            if substituts[rand][5] < nutriscore:
                # Display of random substituts with their parameters
                print(
                    f"\n Et voici le substitut que nous avons trouvé pour le remplacer :\n"
                )
                print(f" - nom: {substituts[rand][1]}")
                print(f" - magasin: {substituts[rand][2]}")
                print(f" - url: {substituts[rand][3]}")
                print(f" - code: {substituts[rand][4]}")
                print(f" - nutriscore: {substituts[rand][5]}")
            elif substituts[rand][5] >= nutriscore or substituts[rand][5] == 0:
                print(
                    f"\n Vous avez déjà choisi un produit avec le meilleur nutriscore \n"
                )
        except TypeError:
            print(
                f"\n Il n'y a actuellement pas de substitut à votre produit dans notre base\n"
            )
            return
        menu_substitut = True
        while menu_substitut:
            if (
                substituts[rand][5] < nutriscore
                or substituts[rand][5] >= nutriscore
                or substituts[rand][5] == "a"
            ):
                try:
                    choix_substitut = input(
                        "Voulez_vous le sauvegarder? O pour Oui/N pour Non\n"
                    )
                    if choix_substitut == "O":
                        # Calling up the menu_favory function
                        self.menu_favory(substituts[rand][0])
                        menu_substitut = False
                    elif choix_substitut == "N":
                        menu_substitut = False
                except ValueError:
                    print("Vous n'avez pas sélectionné de réponse")
                    choix_substitut = input("Voulez_vous le sauvegarder? O/N\n")

    def menu_favory(self, id_product):
        # Function to insert the id_product by calling the set_favory() method.
        # favoris = self.dataBase.set_favory(id_product)
        self.dataBase.set_favory(id_product)

    def display_favory(self):
        """
        Function used to display the list of favoris by calling the get_favory()
        method when the user chose this option.
        """
        list_favory = self.dataBase.get_favory()
        for i in range(len(list_favory)):
            # Display of favoris with their parameters.
            print(f" - nom: {list_favory[i][1]}")
            print(f" - magasin: {list_favory[i][2]}")
            print(f" - url: {list_favory[i][3]}")
            print(f" - code: {list_favory[i][4]}")
            print(f" - nutriscore: {list_favory[i][5]}\n")
            print("**************************************************")

    def run(self):
        # Main menu loop
        menu = True
        while menu:
            # To display a list of options and ask the user to chose one among them.
            try:
                choix = int(
                    input(
                        "1. Rechercher un aliment à remplacer \n"
                        "2. Retrouver mes aliments substitués \n"
                        "0. Quitter le programme\n"
                    )
                )

                if choix == 0:
                    print(
                        "----------------------Merci de votre visite et à bientôt-------------------------------"
                    )
                    menu = False
                if choix == 1:
                    self.menu_category()
                if choix == 2:
                    print(f"\n Voici Vos produits favoris :\n")
                    self.display_favory()

                    input("appuyez entrer pour continuer....")
            except ValueError:
                print("Vous n'avez pas tapé 1 ou 2 ou 0. Veuillez taper 1 ou 2 ou 0")
