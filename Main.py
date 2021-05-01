# !/usr/bin/env python3
# coding:utf-8
from ClassDataBase import DataBase
from ClassAPI import API

def main():
    api = API()
    api.get_products()
    api.cleaner_products()
    cleaned_products = api.get_cleaned_products() 
    api.get_cleaned_products()

    test=DataBase(cleaned_products)
    test.set_Database()
    test.set_tables()
    test.set_product()
    test.set_category()
    test.set_categorized()

    #Lancement de la classe interface

if __name__ == "__main__":
    main()