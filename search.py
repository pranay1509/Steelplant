from sqlalchemy import create_engine
import mysql.connector

# Establish a connection
connectio = mysql.connector.connect(
    host='localhost',
    user='root',
    password='praval@123',
    database='steelplant'
)


def search_emails(email):
    # Connect to your database
    engine = create_engine(connectio)
    connection = engine.connect()

    # Execute the query
    query = f"SELECT * FROM user WHERE email = '{email}'"
    result = connection.execute(query)

    # Retrieve the search results
    results = [row['email'] for row in result]

    # Close the database connection
    connection.close()

    return results

a='mp936@snu.edu.in'
print(search_emails(a))