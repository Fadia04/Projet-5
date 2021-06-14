# !/usr/bin/env python3
# coding:utf-8
from ClassDataBase import DataBase
from ClassAPI import API
from ClassUser import User

def main():
    api = API()
    api.get_products()
    api.cleaner_products()
    cleaned_products = api.get_cleaned_products() 
    api.get_cleaned_products()

    database=DataBase(cleaned_products)
    database.set_Database()
    database.set_tables()
    database.set_product()
    database.set_category()
    database.set_categorized() 
        
    user=User(database)
    user.run()
    user.menu_category()
    user.menu_product()
    user.menu_substitut()


if __name__ == "__main__":
    main()