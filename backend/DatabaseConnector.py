import mysql.connector

class DatabaseConnector:
    def __init__(self, config_loader):
        self.host = config_loader.get_host()
        self.user = config_loader.get_user()
        self.password = config_loader.get_password()
        self.database = config_loader.get_database()
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host, user=self.user, password=self.password, database=self.database
            )
            return self.connection
        except mysql.connector.Error as err:
            print("Error connecting to database:", err)
            return self.connection

    def disconnect(self):
        if self.connection:
            self.connection.close()



