from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

from productmanagementapp import ProductManagementApp
from salesmanagementapp import SalesManagementApp
from usermanagementapp import UserManagementApp


class AdminPanel(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Admin Panel')
        self.setGeometry(100, 100, 400, 200)

        main_layout = QVBoxLayout(self)
        label = QLabel('Welcome to Admin Panel!')
        main_layout.addWidget(label)



        product_management_button = QPushButton('Product Management', self)
        product_management_button.clicked.connect(self.open_product_management)
        main_layout.addWidget(product_management_button)

        sales_management_button = QPushButton('Sales Management', self)
        sales_management_button.clicked.connect(self.open_sales_management)
        main_layout.addWidget(sales_management_button)


        self.product_management_app = None
        self.sales_management_app = None


    def open_sales_management(self):
        # Create UserManagementApp if it doesn't exist
        if not self.sales_management_app:
            self.sales_management_app = SalesManagementApp()

        # Show UserManagementApp
        self.sales_management_app.show()

    def open_product_management(self):
        # Create ProductManagementApp if it doesn't exist
        if not self.product_management_app:
            self.product_management_app = ProductManagementApp()

        # Show ProductManagementApp
        self.product_management_app.show()