import mysql.connector
from getpass import getpass, getuser
import pandas as pd 



def read_database (
        query_file="extraction.sql",
        database="bocchiotti",
        host="127.0.0.1",
        port="3306"
    ):
    """
    Method to read the database and eventually export the 
    results into a .csv.

    :paraam query_file: The .sql file where is writte the query to execute
    :param database: The mysql database name
    :param host: The host IP
    :param port: The port 
    :return: A pandas DataFrame with the database extraction
    """
    # Get user and password to establish the connection with 
    # the database 
    user = input("Username: ")
    password = getpass("Password: ")

    # Get the query string from an .sql file
    with open(query_file, "r") as file:
        query = file.read()

    # Establish a connection with the database and execute the query
    try:
        with mysql.connector.connect(database=database, host=host, port=port,
         user=user, password=password) as connection:
            
            with connection.cursor() as cursor:
                cursor.execute(query)
                #connection.commit()
                df = pd.DataFrame(cursor.fetchall())

    except mysql.connector.Error as err:
        raise err
    
    # Update dataframe columns to standardize the result 
    # with other tests
    df.columns = "OrderID, Code, #Cases, SizeX, SizeY, SizeZ, Weight, Strength, ProdType".split(", ")
    # Return the dataframe
    return df



def db_to_csv (
        csv_file="./bocchiotti_tests/test.csv",
        query_file="extraction.sql",
        database="bocchiotti",
        host="127.0.0.1",
        port="3306"
    ):
    """ Read the database and export the result into a .csv file """
    # Read dataframe
    df = read_database (query_file=query_file, database=database, host=host, port=port)

    # Replace None with Inf on occasion of strength values
    # NOTE: Inf means each item can support an infinite number of other items
    df.replace(to_replace=(None,), value=float("inf"), inplace=True)

    # Export dataframe 
    df.to_csv(csv_file)




if __name__ == '__main__':
    df = read_database(
        query_file="../../../extraction.sql",
        database="bocchiotti",
        host="127.0.0.1",
        port="3306",
        output_file=None
    )
    print(df)
    
    