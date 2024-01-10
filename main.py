import sys

import psycopg2
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton, QMessageBox

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QInputDialog, QMessageBox

from adminpanel import AdminPanel
from product import Product
from productmanagementapp import ProductManagementApp
from salesmanagementapp import SalesManagementApp
from usermanagementapp import UserManagementApp, StaffPanel
from staffpanel import StaffPanel


def main():
    app = QApplication([])

    user_management_app = UserManagementApp()

    # Create instances of AdminPanel and UserManagementApp
    admin_panel = AdminPanel()

    # Connect the signal to show the admin panel
    user_management_app.showAdminPanelSignal.connect(admin_panel.show)
    # Create instances of StaffPanel and UserManagementApp
    staff_panel = StaffPanel()

    # Connect the signal to show the staff panel
    user_management_app.showStaffPanelSignal.connect(staff_panel.show)

    user_management_app.show()
    app.exec_()
if __name__ == '__main__':
   """ app = QApplication(sys.argv)
    user_management_app = UserManagementApp()
    user_management_app.show()

    product_management_app = ProductManagementApp()
    product_management_app.show()

    sales_app = SalesManagementApp()
    sales_app.show()
    sys.exit(app.exec_())"""
   main()
