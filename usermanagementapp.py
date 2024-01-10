import psycopg2
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QMessageBox, QFormLayout, QLabel, QLineEdit

# from adminpanel import AdminPanel
from database import create_connection, close_connection
from staffpanel import StaffPanel


class User:
    def __init__(self, user_id, username, password_hash, role):
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash
        self.role = role


class UserManagementApp(QWidget):
    showAdminPanelSignal = pyqtSignal()
    showStaffPanelSignal = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.current_user = None  # To store the currently logged-in user

        self.setWindowTitle('User Management App')
        self.setGeometry(100, 100, 400, 200)

        main_layout = QVBoxLayout(self)

        self.register_layout = QVBoxLayout()
        main_layout.addLayout(self.register_layout)

        self.init_register_ui()

    def init_register_ui(self):
        form_layout = QFormLayout()

        name_label = QLabel('Username:')
        self.register_username_input = QLineEdit()
        form_layout.addRow(name_label, self.register_username_input)

        password_label = QLabel('Password:')
        self.register_password_input = QLineEdit()
        self.register_password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow(password_label, self.register_password_input)

        role_label = QLabel('Role:')
        self.register_role_input = QLineEdit()
        form_layout.addRow(role_label, self.register_role_input)

        register_button = QPushButton('Register', self)
        register_button.clicked.connect(self.register_user)

        form_layout.addWidget(register_button)

        self.register_layout.addLayout(form_layout)

        # Add login UI
        self.init_login_ui()

    def init_login_ui(self):
        form_layout = QFormLayout()

        name_label = QLabel('Username:')
        self.login_username_input = QLineEdit()
        form_layout.addRow(name_label, self.login_username_input)

        password_label = QLabel('Password:')
        self.login_password_input = QLineEdit()
        self.login_password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow(password_label, self.login_password_input)

        login_button = QPushButton('Login', self)
        login_button.clicked.connect(self.login)

        form_layout.addWidget(login_button)

        self.register_layout.addLayout(form_layout)

    def register_user(self):
        username = self.register_username_input.text()
        password = self.register_password_input.text()
        role = self.register_role_input.text()

        conn = create_connection()

        if conn:
            try:
                cursor = conn.cursor()

                # Example: Check if the username is already taken
                cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
                existing_user = cursor.fetchone()

                if existing_user:
                    self.show_message_box('Registration Failed', 'Username already exists.')
                else:
                    # Example: Insert new user into the database
                    cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)",
                                   (username, password, role))
                    conn.commit()

                    self.show_message_box('Registration Successful', 'User registered successfully.')

            except (Exception, psycopg2.Error) as error:
                print(f"Error executing query: {error}")

            finally:
                close_connection(conn)

    def login(self):
        username = self.login_username_input.text()
        password = self.login_password_input.text()

        conn = create_connection()

        if conn:
            try:
                cursor = conn.cursor()

                # Example: Check if the user exists in the database
                cursor.execute("SELECT * FROM users WHERE username = %s AND password_hash = %s", (username, password))
                result = cursor.fetchone()

                if result:
                    user = User(result[0], result[1], result[2], result[3])
                    self.current_user = user
                    self.show_dashboard()
                else:
                    self.show_message_box('Login Failed', 'Invalid username or password.')

            except (Exception, psycopg2.Error) as error:
                print(f"Error executing query: {error}")

            finally:
                close_connection(conn)

    def show_dashboard(self):
        # Emit the showAdminPanelSignal signal when the user role is admin
        if self.current_user.role == 'admin':
            self.showAdminPanelSignal.emit()
        elif self.current_user.role == 'staff':
            self.showStaffPanelSignal.emit()

    def show_message_box(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()


class Dashboard(QWidget):
    def __init__(self, user):
        super().__init__()

        self.setWindowTitle('Dashboard')
        self.setGeometry(100, 100, 400, 200)

        main_layout = QVBoxLayout(self)
        welcome_label = QLabel(f'Welcome, {user.username}! Role: {user.role}')
        main_layout.addWidget(welcome_label)

        # Add buttons based on the user's role
        if user.role.lower() == 'admin':
            admin_button = QPushButton('Admin Panel', self)
            admin_button.clicked.connect(self.show_admin_panel)
            main_layout.addWidget(admin_button)
        elif user.role.lower() == 'staff':
            staff_button = QPushButton('Staff Panel', self)
            staff_button.clicked.connect(self.show_staff_panel)
            main_layout.addWidget(staff_button)

    def show_admin_panel(self):
        # Implement the functionality for the admin panel
        admin_panel = AdminPanel()
        admin_panel.show()

    def show_staff_panel(self):
        # Implement the functionality for the staff panel
        staff_panel = StaffPanel()
        staff_panel.show()


class AdminPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Admin Panel')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout(self)
        button = QPushButton('Back to User Management', self)
        layout.addWidget(button)

        # Connect the button click to emit a signal
        button.clicked.connect(self.goBackToUserManagement)

    # Define a signal for going back to user management
    goBackToUserManagementSignal = pyqtSignal()

    def goBackToUserManagement(self):
        # Emit the signal when the button is clicked
        self.goBackToUserManagementSignal.emit()


class StaffPanel(QWidget):
    # Define a signal for going back to user management

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Staff Panel')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout(self)
        button = QPushButton('Back to User Management', self)
        layout.addWidget(button)

        # Connect the button click to emit the signal
        button.clicked.connect(self.goBackToUserManagement)

    goBackToUserManagementSignal = pyqtSignal()

    def goBackToUserManagement(self):
        # Emit the signal when the button is clicked
        self.goBackToUserManagementSignal.emit()
