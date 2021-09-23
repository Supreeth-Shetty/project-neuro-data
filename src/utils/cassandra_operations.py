import re
import pandas as pd
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

class cassandra_connect:
    def connect():
        try:
            cloud_config= {'secure_connect_bundle': 'secure-connect-test2.zip'}
            auth_provider = PlainTextAuthProvider('mBdqxsqabXCkOZQZjpsqKFoZ',
                                                  'HWAWizYet0TJ,Pr53r59pdXoWdQRxETe7pYXSyrrz0dZ0hrGaGkgj+7joqUmEPzccZMsR3oN5KsJpvtw,DPcG9tsGRnvsgoIc3iU0J7Gre6IU3B14ZB-wBs-4OCbw6iv')
            cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
            session = cluster.connect('ineuron')
            row = session.execute("select release_version from system.local").one()
            if row:
                print("Connected to Database! - version", row[0])
            else:
                print("An error occured!")
            return session
        except Exception as e:
            print(e)

class query_generator:
    def __init__(self):
        pass

    def create_table_query_csv(self, columns, datatypes, table_name):
        query = f"create table {table_name}("
        object_col = []
        try:
            for i in range(len(datatypes) - 1):
                if len(re.findall(r'\bint\d+', datatypes[i])) > 0:
                    query += f"{columns[i]} int, "
                elif len(re.findall(r'\bfloat\d+', datatypes[i])) > 0:
                    query += f"{columns[i]} float, "
                else:
                    query += f"{columns[i]} text, "
                    object_col.append(list(columns).index(columns[i]))
        except Exception as e:
            return e
        return query.strip() + f" primary key({columns[0]}));", object_col

    def insert_into_generator_csv(self, filepath, object_columns, columns, table_name):

        def insert_statement(columns, filename):
            try:
                query = f"insert into {filename}("
                for col in columns:
                    query += f'{col.replace(" ", "_")}, '
                return query.strip(", '") + ")"
            except Exception as e:
                return e
        try:
            with open(filepath, "r") as file:
                next(file)
                for line in file:
                    data = (line.strip("\n").replace(",,", ",0,").replace('"', '').split(","))
                    for col in object_columns:
                        data[col] = f"'{data[col]}'"
                    yield insert_statement(columns, table_name) + " values(" + ", ".join(data) + ");"
        except Exception as e:
            return e

    def retrive_dataset(self, session, table_name):
        try:
            dataframe = pd.DataFrame(list(session.execute(f'select * from {table_name}')))
            return dataframe
        except Exception as e:
            return e