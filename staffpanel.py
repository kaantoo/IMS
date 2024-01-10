from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

from productmanagementapp import ProductManagementApp



class StaffPanel(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Staff Panel')
        self.setGeometry(100, 100, 400, 200)

        main_layout = QVBoxLayout(self)
        label = QLabel('Welcome to Staff Panel!')
        main_layout.addWidget(label)

        # Add button for Product Management
        product_management_button = QPushButton('Product Management', self)
        product_management_button.clicked.connect(self.open_product_management)
        main_layout.addWidget(product_management_button)

        self.product_management_app = None

    def open_product_management(self):
        # Create ProductManagementApp if it doesn't exist
        if not self.product_management_app:
            self.product_management_app = ProductManagementApp()

        # Show ProductManagementApp
        self.product_management_app.show()
