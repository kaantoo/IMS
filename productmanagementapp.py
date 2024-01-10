import logging
from datetime import datetime

from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.QtWidgets import (
    QWidget, QTableWidget, QPushButton, QVBoxLayout, QTableWidgetItem,
    QInputDialog, QMessageBox
)

from database import create_connection, close_connection
from product import Product


# from supplier_management_dialog import SupplierManagementDialog

class ProductManagementApp(QWidget):
    def __init__(self):
        super().__init__()

        self.products = []
        log_file_path = 'app.log'
        logging.basicConfig(filename=log_file_path, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

        # Create and set up the UI components
        self.product_table = QTableWidget(self)
        self.product_table.setColumnCount(5)
        self.product_table.setHorizontalHeaderLabels(['ID', 'Name', 'Description', 'Price', 'Quantity'])

        self.add_button = QPushButton('Add Product', self)
        self.edit_button = QPushButton('Edit Product', self)
        self.delete_button = QPushButton('Delete Product', self)
        self.sell_button = QPushButton('Sell Product', self)

        # Connect buttons to their respective functions
        self.add_button.clicked.connect(self.add_product_dialog)
        self.edit_button.clicked.connect(self.edit_product)
        self.delete_button.clicked.connect(self.delete_product_dialog)
        self.sell_button.clicked.connect(self.sell_product_dialog)

        # Set up the layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.product_table)
        layout.addWidget(self.add_button)
        layout.addWidget(self.edit_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.sell_button)

        # Load initial products from the database
        self.load_products()

        # Set up a timer for real-time updates (adjust interval as needed)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.load_products)
        self.timer.start(10000)  # Update every 10 seconds (for example)
        product_deleted = pyqtSignal(int)

    def get_product_by_id(self, product_id):
        """Get product information by product ID."""
        for product in self.products:
            if product.product_id == product_id:
                return product
        return None
    def load_products(self):
        """Load products from the database and populate the table."""
        try:
            conn = create_connection()
            if not conn:
                logging.error('Error connecting to the database')
                return

            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM products")
                rows = cursor.fetchall()

                self.products = [Product(*row) for row in rows]
                self.update_product_table()

                self.check_low_stock_levels()
                logging.info('Products loaded successfully')

            except Exception as e:
                logging.error(f"Error executing query to load products: {e}")

        except Exception as er:
            logging.error(f'Error loading products: {er}')

        finally:
            close_connection(conn)

    def check_low_stock_levels(self):
        """Check for low stock levels and display alerts."""
        low_stock_threshold = 10

        try:
            for product in self.products:
                if product.quantity < low_stock_threshold:
                    QMessageBox.warning(self, 'Low Stock Alert',
                                        f"Low stock level for {product.name}. Current quantity: {product.quantity}",
                                        QMessageBox.Ok)
                    self.create_order(product)

            logging.info('Low stock levels checked successfully')
        except Exception as e:
            logging.error(f'Error checking low stock levels: {e}')



    def update_product_table(self):
        """Update the product table with the current products."""
        self.product_table.setRowCount(len(self.products))

        for row, product in enumerate(self.products):
            self.product_table.setItem(row, 0, QTableWidgetItem(str(product.product_id)))
            self.product_table.setItem(row, 1, QTableWidgetItem(product.name))
            self.product_table.setItem(row, 2, QTableWidgetItem(product.description))
            self.product_table.setItem(row, 3, QTableWidgetItem(str(product.price)))
            self.product_table.setItem(row, 4, QTableWidgetItem(str(product.quantity)))

    def add_product_dialog(self):
        """Show a dialog to add a new product."""
        name, ok_name = QInputDialog.getText(self, 'Add Product', 'Enter product name:')
        description, ok_desc = QInputDialog.getText(self, 'Add Product', 'Enter product description:')
        price, ok_price = QInputDialog.getDouble(self, 'Add Product', 'Enter product price:')
        quantity, ok_quantity = QInputDialog.getInt(self, 'Add Product', 'Enter product quantity:')

        if ok_name and ok_desc and ok_price and ok_quantity:
            self.add_product(name, description, price, quantity)

    def add_product(self, name, description, price, quantity):
        """Add a new product to the database."""
        try:
            conn = create_connection()
            if not conn:
                logging.error('Error connecting to the database')
                return

            try:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO products (name, description, price, quantity) VALUES (%s, %s, %s, %s)",
                               (name, description, price, quantity))
                conn.commit()
                logging.info('Product added successfully')

                # Reload products after adding a new one
                self.load_products()

            except Exception as e:
                logging.error(f"Error adding product: {e}")

            finally:
                close_connection(conn)
                # Log inventory changes
                product_id = self.get_last_product_id()
                self.log_inventory_change(product_id, quantity)

        except Exception as er:
            logging.error(f'Error adding product: {er}')

    def edit_product(self):
        """Edit the selected product."""
        selected_row = self.product_table.currentRow()

        if 0 <= selected_row < len(self.products):
            selected_product = self.products[selected_row]

            name, ok_name = QInputDialog.getText(self, 'Edit Product', 'Edit product name:', text=selected_product.name)
            description, ok_desc = QInputDialog.getText(self, 'Edit Product', 'Edit product description:',
                                                        text=selected_product.description)
            price, ok_price = QInputDialog.getDouble(self, 'Edit Product', 'Edit product price:',
                                                     value=selected_product.price)
            quantity, ok_quantity = QInputDialog.getInt(self, 'Edit Product', 'Edit product quantity:',
                                                        value=selected_product.quantity)

            if ok_name and ok_desc and ok_price and ok_quantity:
                self.update_product(selected_product.product_id, name, description, price, quantity)

    def update_product(self, product_id, name, description, price, quantity):
        """Update an existing product in the database."""
        try:
            conn = create_connection()
            if not conn:
                logging.error('Error connecting to the database')
                return

            try:
                cursor = conn.cursor()
                cursor.execute("UPDATE products SET name=%s, description=%s, price=%s, quantity=%s WHERE product_id=%s",
                               (name, description, price, quantity, product_id))
                conn.commit()
                logging.info('Product updated successfully')

                # Reload products after updating
                self.load_products()

            except Exception as e:
                logging.error(f"Error updating product: {e}")

            finally:
                close_connection(conn)
                # Log inventory changes
                self.log_inventory_change(product_id, quantity)

        except Exception as er:
            logging.error(f'Error updating product: {er}')

    def delete_product_dialog(self):
        """Show a dialog to confirm product deletion."""
        selected_row = self.product_table.currentRow()

        if 0 <= selected_row < len(self.products):
            selected_product = self.products[selected_row]

            # Create a confirmation dialog
            reply = QMessageBox.question(self, 'Delete Product',
                                         f"Do you want to delete the product:\n{selected_product.name}?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.delete_product(selected_product.product_id)

    def delete_product(self, product_id):
        """Delete a product from the database."""
        try:
            conn = create_connection()
            if not conn:
                logging.error('Error connecting to the database')
                return

            # Retrieve product information before deletion for logging purposes
            product = self.get_product_by_id(product_id)

            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM products WHERE product_id=%s", (product_id,))
                cursor.execute("DELETE FROM inventory_history WHERE product_id=%s", (product_id,))
                conn.commit()
                logging.info(f'Product "{product.name}" (ID: {product_id}) deleted successfully')

                # Emit signal for product deletion
                self.product_deleted.emit(product_id)

            except Exception as e:
                logging.error(f"Error deleting product: {e}")

            finally:
                close_connection(conn)

                # Log inventory changes only if the product existed before deletion
                if product:
                    self.log_inventory_change(product_id, 0)

        except Exception as er:
            logging.error(f'Error deleting product: {er}')

    def sell_product_dialog(self):
        """Show a dialog to sell a product."""
        selected_row = self.product_table.currentRow()

        if 0 <= selected_row < len(self.products):
            selected_product = self.products[selected_row]

            quantity, ok_quantity = QInputDialog.getInt(self, 'Sell Product', 'Enter quantity to sell:',
                                                        value=1, min=1, max=selected_product.quantity)

            if ok_quantity:
                self.sell_product(selected_product.product_id, selected_product.name, quantity)

    def sell_product(self, product_id, product_name, quantity):
        """Sell a product and update the stock."""
        try:
            conn = create_connection()
            if not conn:
                logging.error('Error connecting to the database')
                return

            try:
                cursor = conn.cursor()

                # Check if the available stock is sufficient
                selected_product = next((p for p in self.products if p.product_id == product_id), None)
                if selected_product and selected_product.quantity >= quantity:
                    # Update the stock in the database
                    new_quantity = selected_product.quantity - quantity
                    cursor.execute("UPDATE products SET quantity=%s WHERE product_id=%s",
                                   (new_quantity, product_id))

                    # Commit the transaction to the database
                    conn.commit()

                    # Log inventory changes
                    self.log_inventory_change(product_id, new_quantity)

                    # Log the sale in the sales history
                    total = selected_product.price * quantity
                    self.log_sales_order(product_name, quantity, total, 'sold')

                    logging.info(f'Product "{product_name}" sold successfully. Quantity: {quantity}')

                    # Check if the stock is low and create a sales order if needed
                    if new_quantity < 10:  # Adjust as needed
                        self.create_sales_order(selected_product, 10)  # You can adjust the quantity as needed

                    # Reload products after selling
                    self.load_products()

                else:
                    QMessageBox.warning(self, 'Insufficient Stock',
                                        f"Insufficient stock for {product_name}. Available quantity: {selected_product.quantity}",
                                        QMessageBox.Ok)

            except Exception as e:
                logging.error(f"Error selling product: {e}")

            finally:
                close_connection(conn)

        except Exception as er:
            logging.error(f'Error selling product: {er}')




    def log_inventory_change(self, product_id, new_quantity):
        """Log inventory changes."""
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()

                # Get the current date and time
                timestamp = datetime.now()

                # Insert a record into the inventory_history table
                cursor.execute(
                    "INSERT INTO inventory_history (product_id, timestamp, new_quantity) VALUES (%s, %s, %s)",
                    (product_id, timestamp, new_quantity))

                conn.commit()
                print("Inventory change logged successfully.")
            except Exception as e:
                print(f"Error logging inventory change: {e}")
            finally:
                close_connection(conn)

    def get_last_product_id(self):
        """Get the last product_id from the products table."""
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT MAX(product_id) FROM products")
                last_product_id = cursor.fetchone()[0]
                return last_product_id if last_product_id is not None else 0
            except Exception as e:
                print(f"Error getting last product_id: {e}")
            finally:
                close_connection(conn)
        return 0

    def create_order(self, product):
        """Create a sales order for a product if the stock level is low."""
        low_stock_threshold = 10  # Adjust as needed

        if product.quantity < low_stock_threshold:
            # Calculate the quantity needed to reach the threshold
            quantity_needed = 10

            # Suggested quantity to order is the quantity needed
            quantity_to_order = quantity_needed

            if quantity_to_order > 0:
                # Create a sales order and update the stock
                total = product.price * quantity_to_order
                #self.log_sales_order(product.name, quantity_to_order, total, 'ordered')

                # Update stock in the database
                new_quantity = product.quantity + quantity_to_order
                self.update_stock_in_database(product.product_id, new_quantity)

                logging.info(f'Sales order created for "{product.name}" - Quantity: {quantity_to_order}, Total: {total}')

                # Reload products after creating the sales order
                self.load_products()

                QMessageBox.information(self, 'Sales Order Created',
                                        f'Sales order created for {product.name}. Quantity: {quantity_to_order}, Total: {total}',
                                        QMessageBox.Ok)
            else:
                QMessageBox.warning(self, 'Insufficient Stock',
                                    f"Insufficient stock for {product.name}. Suggested quantity is 0.",
                                    QMessageBox.Ok)
        else:
            QMessageBox.information(self, 'No Sales Order Needed',
                                    f"No sales order needed for {product.name}. Stock level is sufficient.",
                                    QMessageBox.Ok)

    def update_stock_in_database(self, product_id, new_quantity):
        """Update stock quantity in the database."""
        try:
            conn = create_connection()
            if not conn:
                logging.error('Error connecting to the database')
                return

            try:
                cursor = conn.cursor()
                cursor.execute("UPDATE products SET quantity=%s WHERE product_id=%s",
                               (new_quantity, product_id))
                conn.commit()
                logging.info(f'Stock quantity for product ID {product_id} updated to {new_quantity}')

            except Exception as e:
                logging.error(f"Error updating stock quantity in the database: {e}")

            finally:
                close_connection(conn)

        except Exception as er:
            logging.error(f'Error updating stock quantity in the database: {er}')



