import re
import pandas as pd
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider


class CassandraHelper:
    """
    cassandra_connector class performs cassandra database operations,eg: connecting to database,
    creating table, inserting values into table, retriving dataset for allowed filetypes
    """

    def __init__(self):
        try:
            self.cloud_config = {'secure_connect_bundle': 'secure-connect-test2.zip'}
            self.auth_provider = PlainTextAuthProvider('mBdqxsqabXCkOZQZjpsqKFoZ',
                                                       'HWAWizYet0TJ,Pr53r59pdXoWdQRxETe7pYXSyrrz0dZ0hrGaGkgj+7joqUmEPzccZMsR3oN5KsJpvtw,DPcG9tsGRnvsgoIc3iU0J7Gre6IU3B14ZB-wBs-4OCbw6iv')
            self.cluster = Cluster(cloud=self.cloud_config, auth_provider=self.auth_provider)
            self.keyspace = "ineuron"
        except Exception as e:
            print(e)

    def push_csv_to_database(self, file, table_name):
        """
        [summary]:This functions accepts csv file and table_name and creates table in cassandra with given table_name
        and inserts values from the file given into created table
        Args:
             file ([type]): [file name to upload]
            table_name ([type]): [table name to create ]
        """
        try:
            session = self.cluster.connect(self.keyspace)
            create_table_query = f"create table {table_name}(column_count int, "
            insert_into_table_query = f"insert into {table_name}(column_count , "
            columns = [col + "__dt__" + str(pd.read_csv(file)[col].dtype) for col in pd.read_csv(file).columns]

            for col in columns:
                create_table_query += f"{col} text, "
                insert_into_table_query += f'{col}, '

            query = create_table_query.strip() + f" primary key(column_count));"
            session.execute(query)
            print(f"{table_name} table created")
            query = insert_into_table_query.strip(", '") + ")" + " values(" + str((len(columns) + 1) * ('?,')).strip(", ") + ");"
            prepared_query = session.prepare(query)
            count = 0

            with open(file, "r",encoding='utf-8') as csvfile:
                next(csvfile)
                for line in csvfile:
                    data = (line.strip("\n").replace(",,", ",NaN,").replace('"', '').replace("'", "").split(","))
                    count += 1;
                    data.insert(0, count)
                    try:
                        session.execute(prepared_query, data)
                    except Exception as e:
                        print(e)
            print(f"{count} rows inserted to {table_name} table")
            return 1
        except Exception as e:
            print(e)

        finally:
            if session and not session.is_shutdown:
                session.shutdown()
                print('Cassand session closed!')

    def push_tsv_to_database(self, file, table_name):
        """
        [summary]:This functions accepts tsv file and table_name and creates table in cassandra with given table_name
        and inserts values from the file given into created table
        Args:
            file ([type]): [file name to upload]
            table_name ([type]): [table name to create ]
        """
        try:
            session = self.cluster.connect(self.keyspace)
            create_table_query = f"create table {table_name}(column_count int, "
            insert_into_table_query = f"insert into {table_name}(column_count , "
            columns = ["_".join(i.split()).replace(" ", "") for i in str(pd.read_csv(file).dtypes).split("\n")]
            columns.pop()

            for col in columns:
                create_table_query += f"{col} text, "
                insert_into_table_query += f'{col}, '

            query = create_table_query.strip() + f" primary key(column_count));"
            session.execute(query)
            print(query)
            print("table created")
            query = insert_into_table_query.strip(", '") + ")" + " values(" + str((len(columns) + 1) * ('?,')).strip(", ") + ");"
            print(query)
            prepared_query = session.prepare(query)
            count = 0

            with open(file, "r") as csvfile:
                next(csvfile)
                for line in csvfile:
                    data = (line.strip("\n").replace(",,", ",NaN,").replace('"', '').replace("'", "").split(","))
                    count += 1;
                    data.insert(0, count)
                    try:
                        session.execute(prepared_query, data)
                    except Exception as e:
                        print(e)
        except Exception as e:
            print(e)

        else:
            if not session.is_shutdown:
                session.shutdown()
                print('Cassand session closed!')
                
                

    def retrive_dataset(self, table_name):
        """
        [summary]:This Function will retrieve data from table
        Args:
            table_name ([type]): [name of table]

        Returns:
            [type]: [Pandas DataFrame]
        """
        try:
            session = self.cluster.connect(self.keyspace)
            dataframe = pd.DataFrame(list(session.execute(f'select * from {table_name}'))).drop(columns=['column_count'])
            
            for col in dataframe.columns:
                col_name = col.split("__dt__")[0]
                col_datatype = col.split("__dt__")[1]
                dataframe.rename(columns={col: col_name}, inplace=True)
                try:
                    dataframe[col_name] = dataframe[col_name].astype(col_datatype)
                except Exception as e:
                    print(e)
            return dataframe


        except Exception as e:
            print(e)

        finally:
            if not session.is_shutdown:
                session.shutdown()
                print("cassandra session is closed")



