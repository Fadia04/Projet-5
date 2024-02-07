import requests


class API:
    """
    Class containing functions allowed to import data from Open Food Facts(OFF) API
    and to clean the data imported
    """

    def __init__(self):
        # Class constructor
        self.products = []
        self.cleaned_products = []

    def get_products(self):
        """
        Function to access to OFF and download data according to given parameters
        """
        url = "https://fr.openfoodfacts.org/cgi/search.pl"
        param = {
            "action": "process",
            "sort_by": "unique_scans_n",
            "page_size": 500,
            "page": 1,
            "json": 1,
        }
        req = requests.get(url, param)
        res = req.json()["products"]

        for data in res:
            self.products.append(data)

    def cleaner_products(self):
        """
        Function to select from the products downloaded only those containing the five chosen attributes.
        These data will then be formatted
        """
        for data in self.products:
            if (
                data.get("product_name_fr")
                and data.get("url")
                and data.get("categories")
                and data.get("stores")
                and data.get("nutriscore_grade")
            ):
                data["product_name_fr"] = data.get("product_name_fr").lower()
                data["url"] = data.get("url").lower()
                data["categories"] = data.get("categories").lower()
                data["categories"] = data.get("categories").split(",")
                for i in range(len(data["categories"])):
                    if "'" in data["categories"][i]:
                        data["categories"][i] = data["categories"][i].replace("'", " ")
                data["stores"] = data.get("stores").lower()
                data["nutriscore_grade"] = data.get("nutriscore_grade").lower()
                self.cleaned_products.append(data)

    def get_cleaned_products(self):
        # To return the selected products
        return self.cleaned_products
