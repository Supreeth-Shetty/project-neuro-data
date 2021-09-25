import mysql.connector as connector


"""
    [summary]
        Mysql Helper for all operations related to mysql
    Returns:
        [type]: [None]
"""
class MySqlHelper:
    def __init__(self, host, port, user, password, database):
        """
        [summary]: Constructor
        Args:
            host ([type]): [description]
            port ([type]): [description]
            user ([type]): [description]
            password ([type]): [description]
            database ([type]): [description]
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

    def fetch_all(self, query):
        """
        [summary]: This function will return all record from table
        Args:
            query ([type]): [description]

        Returns:
            [type]: [description]
        """
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
        """
        [summary]:This method return single record from table
        Args:
            query ([type]): [Query to execute]

        Returns:
            [type]: [Data]
        """
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
        """
        [summary]: Function to delete record from table single or multiple
        Args:
            query ([type]): [Query to execute]

        Returns:
            [type]: [No of row effected]
        """
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
        """
        [summary]:Insert record into table
        Args:
            query ([type]): [Query to execute]

        Returns:
            [type]: [1 if row inserted or 0 if not]
        """
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
