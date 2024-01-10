# product.py
from supplier import Supplier

class Product:
    def __init__(self, product_id, name, description, price, quantity, supplier=None):
        self.product_id = product_id
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity
        self.supplier = supplier
