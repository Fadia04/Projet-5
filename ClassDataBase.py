import mysql.connector
import sys
import re


class DataBase:
    def __init__(self, cleaned_products):
        self.database = mysql.connector.connect(host = "localhost", user = "Fadia", password = "Nejm98nedim")
        self.cursor = self.database.cursor(buffered=True)
        self.cleaned_products = cleaned_products
        
    def set_Database(self):
        
        self.cursor.execute("DROP DATABASE IF EXISTS DBP5")
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS DBP5")
        self.cursor.execute("USE DBP5")
        self.database.commit() 

    def set_tables(self):
    
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Product(id_product INT NOT NULL AUTO_INCREMENT, name VARCHAR(255) NOT NULL, stores VARCHAR(255) NOT NULL, url VARCHAR(255) NOT NULL, code INT UNSIGNED, nutriscore VARCHAR(255) NOT NULL,PRIMARY KEY(id_product))ENGINE=InnoDB")
        
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Category(id_category INT NOT NULL AUTO_INCREMENT , name VARCHAR(255) NOT NULL UNIQUE, PRIMARY KEY(id_category))ENGINE=InnoDB")
        
        self.cursor.execute( "CREATE TABLE IF NOT EXISTS Favoris(id_favoris INT NOT NULL AUTO_INCREMENT, id_product INT, PRIMARY KEY(id_favoris), CONSTRAINT FK_ProductFavoris FOREIGN KEY (id_product) REFERENCES Product(id_product))ENGINE=InnoDB")
        
        self.cursor.execute( "CREATE TABLE IF NOT EXISTS Categorized(id_categorized INT AUTO_INCREMENT NOT NULL, id_product INT, id_category INT, PRIMARY KEY(id_categorized), FOREIGN KEY (id_product) REFERENCES Product(id_product), FOREIGN KEY (id_category) REFERENCES Category(id_category))ENGINE=InnoDB") 
    
    
    def set_product(self):
        self.cursor.execute("USE DBP5")                 
        for product in self.cleaned_products:
            add_product = ("INSERT IGNORE INTO Product(name, stores, url, code, nutriscore) VALUES (%(name)s, %(stores)s, %(url)s,%(code)s, %(nutriscore)s)")
            self.product = {

            'name':product["product_name_fr"],
            'stores': product["stores"],
            'url': product["url"],
            'code': product["code"],
            'nutriscore': product["nutriscore_grade"]
                
            }
            self.cursor.execute(add_product,self.product)
            
            self.database.commit()
        #print(self.cursor.rowcount, "record inserted")
    
    def has_cyrillic(self, text):
        return bool(re.search('[\u0400-\u04FF]', text))
    
    def set_category(self):
        self.cursor.execute("USE DBP5")                 
        for product in self.cleaned_products:
            for category in product.get("categories"):
                if not self.has_cyrillic(category):
                    self.cursor.execute(
                    "INSERT IGNORE INTO Category (name) VALUES ('%s');" %  
                    #String
                    (
                        category.strip())
                    )
            
                    self.database.commit()
            
            #print(self.cursor.rowcount, "record inserted")
        
            #self.cursor.close()
            #self.database.close()
   
    def set_categorized(self):
        self.cursor.execute("USE DBP5") 
        for product in self.cleaned_products:
            product_id = (" SELECT (id_product) FROM Product WHERE name =%(name)s")
            self.product = {
            'name': product["product_name_fr"]
            }
            #self.cursor.execute(product_id, self.product)
            
            self.database.commit()
            print(self.cursor.rowcount, "record inserted")
            for category in product.get("categories"):
                if not self.has_cyrillic(category):
                    self.cursor.execute("INSERT IGNORE INTO Categorized( id_category, id_product)  VALUES (%(product_id)s, SELECT id_category FROM Category WHERE name = %(category_name)s",  
                    {'category_name': category.strip(),
                    'product_id': product["product_name_fr"]}, product_id)
                    #return self.cursor.fetchall()
                    self.database.commit()
                    #res = self.cursor.fetchall()
                    #for line in res:
                        #print(line)
                #print(self.cursor.rowcount, "record inserted")
               
    
    def set_categorized(self):
        self.cursor.execute("USE DBP5") 
        for product in self.cleaned_products:        
            product_id = ("INSERT IGNORE INTO Categorized(id_product)" "SELECT (id_product) FROM Product WHERE name =%(name)s")
            self.product={
            'name': product["product_name_fr"]
            }
            self.cursor.execute(product_id, self.product)
           
            self.database.commit()
            print(self.cursor.rowcount, "record inserted")
            for category in product.get("categories"):
                if not self.has_cyrillic(category):
                    self.cursor.execute("INSERT IGNORE INTO Categorized(id_category) SELECT id_category FROM Category WHERE name = %(category_name)s",
                    {'category_name': category.strip()}) #'product_id': product["product_name_fr"]})
                    #return self.cursor.fetchall()
                    #self.database.commit()
                    #res = self.cursor.fetchall()
                    #for line in res:
                        #print(line)
                print(self.cursor.rowcount, "record inserted")
                           
