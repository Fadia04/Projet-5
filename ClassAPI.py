import requests
import json

class API:
    def __init__(self):
        self.products = []
        self.cleaned_products = []
    
    
    def get_products(self):
        url="https://fr.openfoodfacts.org/cgi/search.pl"
        param ={"action": "process",
                    "sort_by": "unique_scans_n",
                    "page_size":5,
                    "page": 1,
                    "json": 1
                }
        req=requests.get(url,param)
        res = req.json()["products"]  
          
        for data in res:
            self.products.append(data)

    def cleaner_products(self):
        for data in self.products:
            if data.get("product_name_fr") and data.get("url") and data.get("categories") and data.get("stores") and data.get("nutriscore_grade"):

                data["product_name_fr"] =  data.get("product_name_fr").lower()
                data["url"] =  data.get("url").lower()
                data["categories"] = data.get("categories").lower()
                data["categories"] = data.get("categories").split(",")
                data["stores"] =  data.get("stores").lower()
                data["nutriscore_grade"] =  data.get("nutriscore_grade").lower()
               
                self.cleaned_products.append(data)
                #print(data["product_name_fr"]) 
                #print(data["categories"])
        #print(len(self.cleaned_products))
          

    def get_cleaned_products(self):
        return self.cleaned_products
       
        


    
"""
a= API()
a.get_products()
a.cleaner_products()
cleaned_products = a.get_cleaned_products() 
a.get_cleaned_products() 
"""
