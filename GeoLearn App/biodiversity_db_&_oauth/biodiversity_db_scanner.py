# pip3 install mysql-connector
import mysql.connector
import csv
from shapely.geometry import Polygon
from shapely.geometry import MultiPolygon
from shapely.geometry import Point
from datetime import datetime
from os import path

DB_FILE_NAME = "biodiversity_mammal_db.csv"
HIST_FILE_NAME = "biodiversity_hist_db.csv" 

# Class that connects to the biodiversity database and creates a 
# local CSV file that contains all the information. 
class biodiversity_db_generator:

        def __init__( self ):
                # connect to our database
                self.database = mysql.connector.connect(
                        host = "ecolocation.c09lpapromur.us-east-2.rds.amazonaws.com",
                        user = "TeamEcolocation",
			password = "EcolocationData",
			port = 3306, 
			database = "ecolocation_data"
			)
                # Create a cursor that we will use to execute commands
                self.db_cursor = self.database.cursor( buffered=True )

                # Create other variables that will be used later
                self.descriptors = []
                self.animal_boundaries = []
                self.animal_info = []
                self.info_merged = []

                # Historic animal data
                self.hist_descriptors = []
                self.hist_boundaries = []
                self.hist_info = []
                self.hist_merged = []

        # Our 'main' function that gathers the information from the database
        # and writes it to a csv
        def generate_db_csv( self ):
                print( "gathering categories" )
                self.get_db_categories()

                print( "gathering boundary information" )
                self.get_db_boundary_info()

                print( "gathering animal information" )
                self.get_db_animal_info()

                print( "merging boundary and animal info" )
                self.merge_info()

                print( "writing to CSV" )
                self.write_to_csv()

                print( "finished" )

        # method to grab the categories/headers of each column
        def get_db_categories( self ):

                # Execute a sql command that returns the categories/headers
                self.db_cursor.execute( "SHOW FIELDS FROM iucn" )

                # Loop through the information from our cursor
                for header in self.db_cursor:

                        # Add the column names to our descriptors variable
                        self.descriptors.append( header[ 0 ] )

                # Execute the sql command that gets the historic animal data
                self.db_cursor.execute( "SHOW FIELDS FROM historic_data" )
                for header in self.db_cursor:
                        self.hist_descriptors.append( header[ 0 ] )

        # method to grab the animal habitat/boundary information
        def get_db_boundary_info( self ):

                # Execute an sql command that returns the boundary information
                self.db_cursor.execute( "SELECT AsText(boundaries) FROM iucn" )

                # Loop through each animal
                for animal in self.db_cursor:

                        # Save its boundary information
                        self.animal_boundaries.append( animal )

                self.db_cursor.execute( "SELECT AsText(boundaries) FROM historic_data" )
                for animal in self.db_cursor:
                        self.hist_boundaries.append( animal )

        def get_db_animal_info( self ):
                # Execute an sql command that returns the animal information
                self.db_cursor.execute( "SELECT * FROM iucn" )

                # Loop through the cursor
                for animal in self.db_cursor:

                        # Save our animal info
                        self.animal_info.append( animal )

                self.db_cursor.execute( "SELECT * FROM historic_data" )
                for animal in self.db_cursor:
                        self.hist_info.append( animal )

        def merge_info( self ):

                # Loop through the database
                for index in range( 0, len( self.animal_boundaries ) ):

                        # Change the tuple animal_info to a list
                        self.info_merged.append( list( self.animal_info[ index ] ) )

                        # Replace the byte data in the animal info with the animal boundary info
                        self.info_merged[ index ][ 17 ] = self.animal_boundaries[ index ]

                for index in range( 0, len( self.hist_boundaries ) ):
                        self.hist_merged.append( list( self.hist_info[ index ] ) )
                        self.hist_merged[ index ][ 4 ] = self.hist_boundaries[ index ]

        def write_to_csv( self ):

                # Create CSV file name
                file_name = DB_FILE_NAME

                # Create a CSV file to write to
                with open( file_name, mode='w' ) as csv_file:

                        # Create our writer object
                        writer = csv.writer( csv_file )

                        # Write the column names in the database
                        writer.writerow( self.descriptors )

                        # Write the row to the csv file
                        writer.writerows( self.info_merged )

                file_name = HIST_FILE_NAME
                with open( file_name, mode='w' ) as csv_file:

                        writer = csv.writer( csv_file )
                        writer.writerow( self.hist_descriptors )
                        writer.writerows( self.hist_merged )
	
generator = biodiversity_db_generator()
generator.generate_db_csv()
#
