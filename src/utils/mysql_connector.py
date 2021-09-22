import mysql.connector as connector


class my_sql_connector:
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

    def fetch_all(self, query):
        try:
            connection = connector.connect(host=self.host, port=self.port, user=self.user,
                                      password=self.password, database=self.database, use_pure=True)
            cursor = connection.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            return data

        except connector.Error as error:
            print("Error: {}".format(error))

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")


    def fetch_one(self, query):
        try:
            connection = connector.connect(host=self.host, port=self.port, user=self.user,
                                      password=self.password, database=self.database, use_pure=True)
            cursor = connection.cursor()
            cursor.execute(query)
            data = cursor.fetchone()
            return data

        except connector.Error as error:
            print("Error: {}".format(error))

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")

    def delete_record(self, query):
        try:
            connection = connector.connect(host=self.host, port=self.port, user=self.user,
                                      password=self.password, database=self.database, use_pure=True)
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            rowcount = cursor.rowcount
            return rowcount

        except connector.Error as error:
            print("Error: {}".format(error))

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")


    def insert_record(self, query):
        try:
            connection = connector.connect(host=self.host, port=self.port, user=self.user,
                                      password=self.password, database=self.database, use_pure=True)
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            rowcount = cursor.rowcount
            return rowcount

        except connector.Error as error:
            print("Error: {}".format(error))

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")
