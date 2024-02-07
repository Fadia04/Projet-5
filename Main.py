# !/usr/bin/env python3
# coding:utf-8
from ClassDataBase import DataBase
from ClassAPI import API
from ClassUser import User


def main():
    # method to make all the classes interact
    api = API()
    # create an object for the API class
    api.get_products()  # to call a function
    api.cleaner_products()
    cleaned_products = api.get_cleaned_products()
    api.get_cleaned_products()

    database = DataBase(cleaned_products)
    # create an object for the DataBase class

    user = User(database)
    # create an object for the User class
    user.reset_database()


if __name__ == "__main__":
    main()
