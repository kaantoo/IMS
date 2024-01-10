import logging
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtWidgets import QWidget, QTableWidget, QPushButton, QVBoxLayout, QTableWidgetItem, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from database import create_connection, close_connection
from product import Product

class SalesManagementApp(QWidget):
    def __init__(self):
        super().__init__()

        self.sales_orders = []

        # Create and set up the UI components
        self.sales_table = QTableWidget(self)
        self.sales_table.setColumnCount(5)
        self.sales_table.setHorizontalHeaderLabels(['Order ID', 'Product', 'Quantity', 'Total', 'Price'])

        self.view_sales_button = QPushButton('View Sales History', self)
        self.generate_report_button = QPushButton('Generate Sales Report', self)

        # Connect buttons to their respective functions
        self.view_sales_button.clicked.connect(self.view_sales_history)
        self.generate_report_button.clicked.connect(self.generate_sales_report)
        self.generate_sales_report_button = QPushButton('Generate Sales Report', self)
        self.generate_stock_report_button = QPushButton('Generate Stock Report', self)
        self.generate_profitability_report_button = QPushButton('Generate Profitability Report', self)
        self.visualize_data_button = QPushButton('Visualize Data with Charts', self)

        # Connect buttons to their respective functions
        self.generate_sales_report_button.clicked.connect(self.generate_sales_report)
        self.generate_stock_report_button.clicked.connect(self.generate_stock_report)
        self.generate_profitability_report_button.clicked.connect(self.generate_profitability_report)
        self.visualize_data_button.clicked.connect(self.visualize_data_with_charts)
        self.restock_suggestions_button = QPushButton('Restock Suggestions', self)
        self.restock_suggestions_button.clicked.connect(self.generate_restock_suggestions)

        # Add report buttons to the layout

        # Set up the layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.sales_table)
        layout.addWidget(self.view_sales_button)
        layout.addWidget(self.generate_report_button)
        layout.addWidget(self.generate_sales_report_button)
        layout.addWidget(self.generate_stock_report_button)
        layout.addWidget(self.generate_profitability_report_button)
        layout.addWidget(self.visualize_data_button)
        layout.addWidget(self.restock_suggestions_button)

        # For data visualization
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Set up logging
        logging.basicConfig(filename='sales_management.log', level=logging.INFO)

    def view_sales_history(self):
        logging.info("Viewing sales history.")

        # Clear the existing sales orders before loading new data
        self.sales_orders = []

        # Load sales history from the database
        conn = create_connection()

        if conn:
            try:
                cursor = conn.cursor()

                # Execute SQL query to fetch sales history
                cursor.execute(
                    "SELECT sales_history.order_id, sales_history.quantity, sales_history.total, "
                    "products.product_id, products.name, products.price "
                    "FROM sales_history "
                    "JOIN products ON sales_history.product_id = products.product_id"
                )

                # Fetch all rows
                rows = cursor.fetchall()

                # Populate the sales orders list
                self.sales_orders = [{'order_id': row[0], 'quantity': row[1], 'total': row[2],
                                      'product_id': row[3], 'product_name': row[4], 'price': row[5]} for row in rows]

                # Update the sales table in the UI
                self.update_sales_table()

                print("Sales history loaded successfully.")

            except Exception as e:
                logging.error(f"Error loading sales history: {e}")

            finally:
                close_connection(conn)
        else:
            logging.error("Error connecting to the database")

    def update_sales_table(self):
        self.sales_table.setRowCount(len(self.sales_orders))

        for row, order in enumerate(self.sales_orders):
            self.sales_table.setItem(row, 0, QTableWidgetItem(str(order['order_id'])))
            self.sales_table.setItem(row, 1, QTableWidgetItem(order['product_name']))
            self.sales_table.setItem(row, 2, QTableWidgetItem(str(order['quantity'])))
            self.sales_table.setItem(row, 3, QTableWidgetItem(str(order['total'])))
            self.sales_table.setItem(row, 4, QTableWidgetItem(str(order['price'])))

    """def generate_sales_report(self):
        labels = [order['product_name'] for order in self.sales_orders]
        quantities = [order['quantity'] for order in self.sales_orders]

        self.ax.clear()
        self.ax.bar(labels, quantities, color='blue')
        self.ax.set_xlabel('Product')
        self.ax.set_ylabel('Quantity')
        self.ax.set_title('Sales Report')

        self.canvas.draw()"""

    def log_sales_order(self, product_name, quantity, total, status):
        """Log a sales order in the sales history table."""
        try:
            conn = create_connection()
            if not conn:
                logging.error('Error connecting to the database')
                return

            try:
                cursor = conn.cursor()

                # Get the current date and time
                timestamp = datetime.now()

                # Insert a record into the sales_history table
                cursor.execute(
                    "INSERT INTO sales_history (product_name, quantity, total, timestamp, status) VALUES (%s, %s, %s, %s, %s)",
                    (product_name, quantity, total, timestamp, status))

                conn.commit()
                logging.info(
                    f"Sales order logged successfully: Product '{product_name}', Quantity: {quantity}, Total: {total}")

            except Exception as e:
                logging.error(f"Error logging sales order: {e}")

            finally:
                close_connection(conn)

        except Exception as er:
            logging.error(f'Error logging sales order: {er}')

    def generate_sales_report(self):
        # Placeholder for sales report logic
        logging.info("Generating sales report.")

        # Implement logic to query sales data from the database
        sales_data = self.query_sales_data_from_database()

        # Generate a bar chart for sales data
        products = [item['product'] for item in sales_data]
        quantities = [item['quantity'] for item in sales_data]

        plt.bar(products, quantities, color='green')
        plt.xlabel('Product')
        plt.ylabel('Quantity')
        plt.title('Sales Report')
        plt.show()

    def generate_stock_report(self):
        # Placeholder for stock report logic
        logging.info("Generating stock report.")

        # Implement logic to query stock data from the database
        stock_data = self.query_stock_data_from_database()

        # Generate a bar chart for stock data
        products = [item['product'] for item in stock_data]
        quantities = [item['quantity'] for item in stock_data]

        plt.bar(products, quantities, color='blue')
        plt.xlabel('Product')
        plt.ylabel('Quantity')
        plt.title('Stock Report')
        plt.show()

    def generate_profitability_report(self):
        # Placeholder for profitability report logic
        logging.info("Generating profitability report.")

        # Implement logic to query profitability data from the database
        profitability_data = self.query_profitability_data_from_database()

        # Generate a bar chart for profitability data
        products = [item['product'] for item in profitability_data]
        profits = [item['profit'] for item in profitability_data]

        plt.bar(products, profits, color='orange')
        plt.xlabel('Product')
        plt.ylabel('Profit')
        plt.title('Profitability Report')
        plt.show()

    def visualize_data_with_charts(self):
        # Placeholder for data visualization logic
        logging.info("Visualizing data with charts.")

        # Implement logic to query data for visualization from the database
        data_for_visualization = self.query_data_for_visualization_from_database()

        # Generate a scatter plot for visualization
        plt.scatter(data_for_visualization[:, 0], data_for_visualization[:, 1], color='red')
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.title('Data Visualization with Charts')
        plt.show()

    def query_sales_data_from_database(self):
        conn = create_connection()
        sales_data = []

        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT product_name, SUM(quantity) AS quantity FROM sales_orders GROUP BY product_name"
                )
                rows = cursor.fetchall()

                sales_data = [{'product': row[0], 'quantity': row[1]} for row in rows]

            except Exception as e:
                logging.error(f"Error querying sales data: {e}")

            finally:
                close_connection(conn)

        return sales_data

    def query_stock_data_from_database(self):
        conn = create_connection()
        stock_data = []

        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT product_name, quantity FROM products"
                )
                rows = cursor.fetchall()

                stock_data = [{'product': row[0], 'quantity': row[1]} for row in rows]

            except Exception as e:
                logging.error(f"Error querying stock data: {e}")

            finally:
                close_connection(conn)

        return stock_data

    def query_profitability_data_from_database(self):
        conn = create_connection()
        profitability_data = []

        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT product_name, SUM(total) AS profit FROM sales_history GROUP BY product_name"
                )
                rows = cursor.fetchall()

                profitability_data = [{'product': row[0], 'profit': row[1]} for row in rows]

            except Exception as e:
                logging.error(f"Error querying profitability data: {e}")

            finally:
                close_connection(conn)

        return profitability_data

    def query_data_for_visualization_from_database(self):
        conn = create_connection()
        data_for_visualization = np.array([])

        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT column1, column2 FROM reports"
                )
                rows = cursor.fetchall()

                data_for_visualization = np.array(rows)

            except Exception as e:
                logging.error(f"Error querying data for visualization: {e}")

            finally:
                close_connection(conn)

        return data_for_visualization

    def generate_restock_suggestions(self):
        # Adjusted logic to generate restocking suggestions based on inventory levels
        low_stock_threshold = 10  # Threshold to trigger the restocking suggestion
        critical_stock_threshold = 15  # Threshold to display the suggestion

        conn = create_connection()

        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT name, quantity FROM products WHERE quantity < %s AND quantity < %s",
                               (low_stock_threshold, critical_stock_threshold))
                rows = cursor.fetchall()

                if rows:
                    suggestions = [f"{row[0]}: {critical_stock_threshold - row[1]} units needed" for row in rows]
                    QMessageBox.information(self, 'Restocking Suggestions', '\n'.join(suggestions), QMessageBox.Ok)
                else:
                    QMessageBox.information(self, 'Restocking Suggestions', 'No restocking suggestions at the moment.',
                                            QMessageBox.Ok)

            except Exception as e:
                logging.error(f"Error generating restocking suggestions: {e}")
                QMessageBox.warning(self, 'Error', f'Error generating restocking suggestions: {e}', QMessageBox.Ok)

            finally:
                close_connection(conn)


