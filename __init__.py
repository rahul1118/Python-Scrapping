
from builtins import object
import csv
from amazonscraper.client import Client


__version__ = '0.1.2'  


class Products(object):
    """Class of the products"""
    def __init__(self, product_dict_list=[]):
        self.products = []
        self.last_html_page = ""  # HTML content of the last scraped page
        self.html_pages = []
        for product_dict in product_dict_list:
            self._add_product(product_dict)

    def _add_product(self, product_dict):
      
        product = Product(product_dict)
        self.products.append(product)

    def __len__(self):
        return len(self.products)

    def __getitem__(self, key):
       
        return self.products[key]

    def csv(self, file_name, separator=","):

        if not self.products:
            return

        with open(file_name, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=separator)

            header = list(self.products[0].product.keys())
            writer.writerow(header)

            for product in self.products:
                writer.writerow(list(product.product.values()))

class Product(object):
    def __init__(self, product_dict={}):
        self.product = product_dict

    def __getattr__(self, attr):
       
        return self.product.get(attr, "")


def search(keywords="", search_url="", max_product_nb=100):
   
    amz = Client()
    product_dict_list = amz._get_products(
        keywords=keywords,
        search_url=search_url,
        max_product_nb=max_product_nb)
    products = Products(product_dict_list)
    products.html_pages = amz.html_pages
    products.last_html_page = amz.html_pages[-1]

    return products
