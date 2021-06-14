import mysql.connector
import re
from random import *



class DataBase:
    def __init__(self, cleaned_products):
        self.database = mysql.connector.connect(
            host="localhost", user="Fadia", password="Nejm98nedim"
        )
        self.cursor = self.database.cursor(buffered=True)
        self.cleaned_products = cleaned_products
    
    def set_Database(self):

        self.cursor.execute("DROP DATABASE IF EXISTS DBP5")
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS DBP5")
        self.cursor.execute("USE DBP5")
        self.database.commit()

    def set_tables(self):

        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS Product(id_product INT NOT NULL AUTO_INCREMENT, name VARCHAR(255) NOT NULL UNIQUE, stores VARCHAR(255) NOT NULL, url VARCHAR(255) NOT NULL, code INT UNSIGNED, nutriscore VARCHAR(255) NOT NULL,PRIMARY KEY(id_product))ENGINE=InnoDB"
        )

        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS Category(id_category INT NOT NULL AUTO_INCREMENT , name VARCHAR(255) NOT NULL UNIQUE , PRIMARY KEY(id_category))ENGINE=InnoDB"
        )

        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS Favoris(id_favoris INT NOT NULL AUTO_INCREMENT, id_product INT, PRIMARY KEY(id_favoris), CONSTRAINT FK_ProductFavoris FOREIGN KEY (id_product) REFERENCES Product(id_product))ENGINE=InnoDB"
        )

        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS Categorized(id_categorized INT AUTO_INCREMENT NOT NULL, id_product INT, id_category INT, PRIMARY KEY(id_categorized), FOREIGN KEY (id_product) REFERENCES Product(id_product), FOREIGN KEY (id_category) REFERENCES Category(id_category))ENGINE=InnoDB"
        )

    def set_product(self):
        self.cursor.execute("USE DBP5")
        for product in self.cleaned_products:
            add_product = "INSERT IGNORE INTO Product(name, stores, url, code, nutriscore) VALUES (%(name)s, %(stores)s, %(url)s,%(code)s, %(nutriscore)s)"
            self.product = {
                "name": product["product_name_fr"],
                "stores": product["stores"],
                "url": product["url"],
                "code": product["code"],
                "nutriscore": product["nutriscore_grade"],
            }
            self.cursor.execute(add_product, self.product)

            self.database.commit()

    def has_cyrillic(self, text):
        return bool(re.search("[\u0400-\u04FF]", text))
   
    def set_category(self):
        self.cursor.execute("USE DBP5")
        for product in self.cleaned_products:
            for category in product.get("categories"):
                if not self.has_cyrillic(category):
                    self.cursor.execute(
                        "INSERT IGNORE INTO Category (name) VALUES ('%s');"%
                        (category.strip(),)
                    )

                    self.database.commit()

    def set_categorized(self):
        self.cursor.execute("USE DBP5")
        for product in self.cleaned_products:
            add=" SELECT DISTINCT Product.id_product FROM Product WHERE Product.name = %(name)s "
            self.product ={"name": product["product_name_fr"]}
            self.cursor.execute(add, self.product)
            self.database.commit()
            product_id = self.cursor.fetchone()
            for category in product.get("categories"):
                if not self.has_cyrillic(category):
                    category_id = self.cursor.execute(
                        "SELECT DISTINCT Category.id_category FROM Category WHERE name= ('%(name)s');"
                        % {"name": category.strip()}
                    )
                    category_id = self.cursor.fetchone()
                    self.cursor.execute(
                        "INSERT INTO Categorized(id_product, id_category)  VALUES ('%(product_id)s','%(category_id)s');"
                        % {'product_id': product_id[0], 'category_id': category_id[0]}
                    )
                    self.database.commit()
        
    def get_category(self):
        self.cursor.execute("USE DBP5")
        self.cursor.execute("SELECT id_category, name FROM Category ORDER BY RAND() LIMIT 5")
        return self.cursor.fetchall()
    def print_category(self):
        categories = self.get_category()
        print(categories)

    def get_id_product(self, id_category):
        self.cursor.execute("USE DBP5")                
        sql=("SELECT id_product FROM Categorized WHERE id_category=%(id)s ORDER BY RAND() LIMIT 5;"% {'id':id_category})
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_product(self, id_category):
        self.cursor.execute("USE DBP5")
        products =[]                
        for id_product in self.get_id_product(id_category):
            self.cursor.execute("SELECT * FROM Product WHERE id_product = '%(id_product)s';"% {'id_product': id_product[0]})
            products.append(self.cursor.fetchone())
            #print(self.cursor.fetchone())
            #print(products)            
        return products
   
    def get_id_substitut(self,id_product, id_category):
        self.cursor.execute("USE DBP5")
        id_substituts = [] 
        self.cursor.execute("SELECT id_product FROM Categorized  WHERE id_product != '%(id_product)s' AND id_category = %(id)s;" % {'id_product': id_product, 'id': id_category})
        id_substituts.append(self.cursor.fetchall())
        #print(id_substituts)
        return id_substituts

    def get_substitut(self, id_product, id_category, nutriscore):
        self.cursor.execute("USE DBP5")
        substituts=[]
        for id_product in self.get_id_substitut(id_product, id_category)[0]:
            print(id_product)
            self.cursor.execute("SELECT * FROM Product WHERE id_product = '%(id_product)s' AND nutriscore <= '%(nutriscore)s';"% {'id_product': id_product[0], 'nutriscore':nutriscore})
            substituts.append(self.cursor.fetchone())
            print(substituts)
        return substituts

    def set_favory(self,id_product):
        self.cursor.execute("USE DBP5")
        self.cursor.execute(
        "INSERT INTO Favoris(id_product) VALUES ('%(id_product)s');"% {'id_product': id_product})
        self.database.commit()
    def get_favory(self):
        self.cursor.execute("USE DBP5")
        favoris = []
        self.cursor.execute("SELECT * FROM Product INNER JOIN Favoris ON Product.id_product = Favoris.id_product")
        favoris.append(self.cursor.fetchall())
        self.database.commit()
        print(favoris)
        return favoris
        