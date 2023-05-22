import os
import argparse
import psycopg2

def select_students(dbname, user, password, host, port):
    # Establish a connection to the database
    try:
        conn = psycopg2.connect(
            dbname=dbname, 
            user=user, 
            password=password, 
            host=host, 
            port=port
        )

        cur = conn.cursor()

        # Execute the SQL query
        cur.execute("SELECT id,first_name,last_name,professor_onyen FROM student ORDER BY last_name,first_name")

        # Fetch all the rows
        rows = cur.fetchall()

        for row in rows:
            print(f"ID: {row[0]}, First Name: {row[1]}, Last Name: {row[2]}, Professor ONYEN: {row[3]}")

        # Close the connection
        cur.close()
        conn.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def main():
    parser = argparse.ArgumentParser(description='Select students from database.')
    parser.add_argument('-d', '--dbname', default=os.getenv('DB_NAME'), help='Database name')
    parser.add_argument('-u', '--user', default=os.getenv('DB_USER'), help='Database user')
    parser.add_argument('-p', '--password', default=os.getenv('DB_PASSWORD'), help='Database password')
    parser.add_argument('-H', '--host', default=os.getenv('DB_HOST'), help='Database host')
    parser.add_argument('-P', '--port', default='5432', help='Database port (default is 5432)')
    args = parser.parse_args()

    # Call the function with command line arguments
    select_students(args.dbname, args.user, args.password, args.host, args.port)



if __name__ == "__main__":
    main()
