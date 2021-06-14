from ClassDataBase import DataBase
import mysql.connector
from random import *

class User:
    def __init__(self, dataBase): 
        self.dataBase = dataBase
        

    def menu_category(self):
        categories = self.dataBase.get_category() 
        for i in range(len(categories)):
            print(f"{i+1} - {categories[i][1]}")

        menu_category = True
        while menu_category:
            try:
                choix_category=(int(input("Sélectionner un numéro de catégorie entre 1 et 5 \n")))
                if choix_category > 0 <=(len(categories)):      
                    self.menu_product(categories[choix_category-1][0])                       
            except ValueError:
                print("Vous n'avez pas choisi de nombre entre 1 et 5") 
                choix_category=(int(input("Sélectionner un numéro de catégorie entre 1 et 5 \n")))
            
    def menu_product(self, id_category): 
        products = self.dataBase.get_product(id_category)          
        for i in range(len(products)):
            print(f"{i+1} - {products[i][1]}")
            
        menu_product = True
        while menu_product:
            try:
                choix_product=(int(input("Sélectionnez un produit\n"))) 
                print(f" Votre produit:")                
                print(f" - id: {products[choix_product-1][0]}")            
                print(f" - nom: {products[choix_product-1][1]}")
                print(f" - magasin : {products[choix_product-1][2]}")
                print(f" - url: {products[choix_product-1][3]}")
                print(f" - code: {products[choix_product-1][4]}")
                print(f" - nutriscore: {products[choix_product-1][5]}")
                if products[choix_product-1][5] == "a":
                    print("Vous avez déjà choisi un produit avec le meilleur nutriscore")
                else:    
                    print("Votre substitut")
                    self.menu_substitut(products[choix_product-1][0], id_category, products[choix_product-1][5])
                    
            except ValueError:
                print("Vous n'avez pas sélectionné de produit")
                choix_product=(int(input("Sélectionnez un produit")))                 

    def menu_substitut(self,id_product, id_category, nutriscore):        
        substituts = self.dataBase.get_substitut(id_product, id_category, nutriscore)
        rand = randint(0,len(substituts)-1)
        #for i in range(len(substituts)):
        print("len:  ",len(substituts))
        
        if substituts[rand][5]>nutriscore :
            print("xxxx")
        else:
            print(f" - nom: {substituts[rand][1]}")
            print(f" - magasin: {substituts[rand][2]}")
            print(f" - url: {substituts[rand][3]}")
            print(f" - code: {substituts[rand][4]}")
            print(f" - nutriscore: {substituts[rand][5]}")    
            
        if substituts ==0:
            print("La base de données ne contient aucun substitut à votre produit")
        menu_substitut = True
        while menu_substitut:
            try: 
                choix_substitut =(input("Voulez_vous le sauvegarder? O/N\n"))
                if choix_substitut == "O":
                    self.menu_favory(substituts[rand][0])                    
                    self.run()
                elif choix_substitut =="N":
                    self.menu_product(id_category)
                else:
                    print("Vous n'avez pas donné de réponse, veuillez recommencer")
                   
            except ValueError:
                print("Vous n'avez pas sélectionné de produit")
                choix_product=(int(input("Sélectionnez un produit"))) 
          
               
    def menu_favory(self, id_product):
        favoris = self.dataBase.set_favory(id_product)            
    
    def run(self):        
        menu = True
        
        while menu:       
            try:
                choix = int(input("1. Quel aliment souhaitez vous remplacer? \n"
                                "2. Retrouver mes aliments substitués \n"
                                "0. Quitter le programme\n"))
                print("----------------------Fin-------------------------------")
                if choix == 0:
                    menu = False
                
                if choix == 1:
                    self.menu_category()
                if choix ==2:
                    self.dataBase.get_favory()
            except ValueError:
                print("Vous n'avez pas tapé 1 ou 2 ou 0. Veuillez taper 1 ou 2 ou 0")
             

            