import csv
import mysql.connector


DB_NAME = "biodiversity_mammal_db.csv" 

def main():
    sort_db()

def sort_db():

    # Open the databases
    database = mysql.connector.connect(
        host = "ecolocation.c09lpapromur.us-east-2.rds.amazonaws.com",
        user = "TeamEcolocation",
        password = "EcolocationData",
        port = 3306,
        database = "ecolocation_data" 
        )

    # Loop through all of the rows
    cursor = database.cursor( buffered=True )

    # Check if the animal is extinct
    cursor.execute( "SHOW TABLES" )

    for thing in cursor:

        print( thing[ 0 ] )

    print()

    cursor.execute( "SHOW FIELDS FROM historic_data" )

    for thing in cursor:

        print( thing[ 0 ] )

    cursor.execute( "SHOW FIELDS FROM iucn" )
    print()
    
    for thing in cursor:

        print( thing[ 0 ] )

    # If it is, then add to the counter 

if __name__ == "__main__":
    main()
