import mysql.connector
import csv
import sys
import os

# pip3 install shapely
from shapely.geometry import Polygon
from shapely.geometry import MultiPolygon
from shapely.geometry import Point
from datetime import datetime

# pip3 install pydrive
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

def main(): 
	find_animals_main()

def find_animals_main():

	# constant for testing database executions 
	ROWS_TO_ACCESS = 1
	
	# The size of the area that we want to search for 
	# 1 about equals 70 miles  (69.4)
	SEARCH_RADIUS = 1
	
	# Our boolean that maintains the main loop 
	getting_info = True

	descriptors = []
	animal_boundaries = []
	animal_info = []
	
	'''
	# connect to our database
	mydb = mysql.connector.connect(
	
		host="ecolocation.c09lpapromur.us-east-2.rds.amazonaws.com",
		user="TeamEcolocation",
		password="EcolocationData",
		port=3306,
		database="ecolocation_data"
		)

	# Create a cursor to look through the database
	mycursor = mydb.cursor( buffered=True )
	 
	# Grab the descriptors of the mammals information from the database
	descriptors = []
	mycursor.execute( "SHOW FIELDS FROM iucn" )
	for x in mycursor: 
		descriptors.append( x[ 0 ] )
		
	animal_boundaries = []
	animal_info = []
	
	
	print( "starting animal boundary shape file creation" )
	mycursor.execute( "SELECT AsText(boundaries) FROM iucn LIMIT %d" % (ROWS_TO_ACCESS) )
	
	#mycursor.execute( "SELECT AsText(boundaries) FROM iucn" )
	for animal in mycursor:
		animal_boundaries.append( create_shape( animal ) )
	print( "done" )
	
	
	
	
	#mycursor.execute( "SELECT * FROM iucn LIMIT %d" % (ROWS_TO_ACCESS) )
	mycursor.execute( "SELECT * FROM iucn" )
	print( "starting animal information extraction" )
	for animal in mycursor:
		animal_info.append( animal )
	print( "done" )
	'''
	
	print( "beginning local db read" )
	
	with open( "biodiversity_mammal_db.csv" ) as csvFile: 
		csv.field_size_limit( sys.maxsize )
		csv_reader = csv.reader( csvFile )
		
		index = 0
		
		for row in csv_reader: 
			if index == 0:
				descriptors = row
			else:
				animal_info.append( row )
				animal_boundaries.append( create_shape(animal_info[ index - 1 ][17]) )
				
			index += 1
			
			if index % 1000 == 0:
				print( "read in " + str( index ) + " animals" )
			
	print( "finished reading database" )
	
	while getting_info:
	
		animals_within_boundaries = []
		print( "Enter latitude and longitude (comma separated) or \"exit\" to exit: " )
		response = input()
		if response.lower() == "exit":
			getting_info = False
		else:
			try: 
				response = response.split( "," )
				latitude = float( response[ 0 ] )
				longitude = float( response[ 1 ] )
				
				#count = 0
				for index in range( 0, len( animal_boundaries ) ):
				
					#count += 1
					#print( count, end= " " )
					
					if checkCoordinates_in_animalInfo( longitude, latitude, animal_boundaries[ index ], SEARCH_RADIUS ):
						animals_within_boundaries.append( animal_info[ index ] )
								
				if len( animals_within_boundaries ) == 0:
					print( "There were no mammals in that area" )
				else:
					filename = write_mammal_info_to_csv( animals_within_boundaries, descriptors, latitude, longitude )
					send_csv_to_drive( filename )
					#display_mammal_information( animals_within_boundaries, descriptors )
					print( "number of animals" )
					print( len( animals_within_boundaries ) )
			except ValueError: 
				print( "Please input a valid latitude and longitude or \"Exit\" " )	
	
# end main 	

def find_animals_script( latitude, longitude ):
	# constant for testing database executions 
	ROWS_TO_ACCESS = 1
	
	# The size of the area that we want to search for 
	# 1 about equals 70 miles  (69.4)
	SEARCH_RADIUS = 1
	
	# Our boolean that maintains the main loop 
	getting_info = True

	descriptors = []
	animal_boundaries = []
	animal_info = []
	
	print( "beginning local db read" )
	
	with open( "biodiversity_db_&_oauth/biodiversity_mammal_db.csv" ) as csvFile: 
		csv.field_size_limit( sys.maxsize )
		csv_reader = csv.reader( csvFile )
		
		index = 0
		
		for row in csv_reader: 
			if index == 0:
				descriptors = row
			else:
				animal_info.append( row )
				animal_boundaries.append( create_shape(animal_info[ index - 1 ][17]) )
				
			index += 1
			
			if index % 1000 == 0:
				print( "read in " + str( index ) + " animals" )
			
	print( "finished reading database" )

	animals_within_boundaries = []

	try: 
			
		for index in range( 0, len( animal_boundaries ) ):
					
			if checkCoordinates_in_animalInfo( longitude, latitude, animal_boundaries[ index ], SEARCH_RADIUS ):
				animals_within_boundaries.append( animal_info[ index ] )
								
		if len( animals_within_boundaries ) == 0:
			print( "There were no mammals in that area" )
		else:
			filename = write_mammal_info_to_csv( animals_within_boundaries, descriptors, latitude, longitude )
			send_csv_to_drive( filename )
			#display_mammal_information( animals_within_boundaries, descriptors )
			print( "number of animals" )
			print( len( animals_within_boundaries ) )
			
			return filename + '.csv'
			
	except ValueError: 
		print( "Please input a valid latitude and longitude or \"Exit\" " )	

# Check if an animal's habitat area is within the area we're searching 
def checkCoordinates_in_animalInfo( latitude, longitude, animal_boundary, search_radius ):
	
	# create a polygon object originating from the latitude and longitude
	origin_point = Point( latitude, longitude )
	
	# Create a circle that will be where we search for animal habitats
	search_area = origin_point.buffer( search_radius )
	
	# Turn this circle into a polygon object that can be used to check if it
	# intersects with an animal's polygon object that represents its habitat
	search_polygon = Polygon( list( search_area.exterior.coords ) )

	# Check if the animal's boundary is unusable
	if animal_boundary.is_valid == False:
	
		# If so, just return false 
		return False
	
	# Otherwise, check if our search area intersects with the animal's habitat
	return search_polygon.intersects( animal_boundary )

# Print the animal's information to the commandline 
def display_mammal_information( listOfMammals, descriptors ):

	for x in listOfMammals: 
		for index in range( 0, len( x )):
			if index != 17:	
				print( " - " + descriptors[ index ], end= ": " )
				print( x[ index ] )
		
		print( "\n====================\n" )

# Write our found animals' information to a CSV file 
def write_mammal_info_to_csv( listOfMammals, descriptors, latitude, longitude ):

        # Variables
        now = datetime.now() 
        list_of_mammals_cleaned = []; 

        # Create CSV file name 
        # Add the date and time to ensure that the file names are unique
        #file_wo_extension = "mammal_info_" + now.strftime( "%d-%m-%Y %H-%M-%S" )
        file_wo_extension = "mammal_info_" + str( latitude ) + '_' + str( longitude )
        file_name = file_wo_extension + ".csv"
	
        # Create a CSV file to write to 
        with open( file_name, mode='w' ) as csv_file: 
                writer = csv.writer( csv_file )
		
                # Write the latitude and longitude to the CSV
                #writer.writerow( [ latitude, longitude ] )
		
                # Delete the 17th column in the descriptors 
                headers = list( descriptors )
                headers.pop( 17 )	
			
                # Write the descriptors/headers to the file 
                writer.writerow( headers )
		
                # Loop through each animal we found 
                for animal in listOfMammals:
			
                        # Create a list of the animal's info 
                        mammal_info = list( animal )
			
                        # Delete the 17th index, the shape files 
                        mammal_info.pop( 17 )
			
                        # Write the information to the row in the CSV
                        writer.writerow( mammal_info )	
			
        # Print to the user that the CSV file has been printed
        print( "done writing to CSV file" )
	
        return file_wo_extension
		
# Creates a polygon object from our database's shape file parameters
def create_polygon( currentShape ):

	listOf_shapesPoints = []
	# Separate our list of coordinates into the shell and the holes
	shapeList = currentShape.strip( "('POLYGON((" ).strip( "))',)" ).split( ")" )
	
	# Delete all of the empty elements in the list 
	listIndex = 0
	for	i in range( 0, len( shapeList ) ):
	
		# If an element in the list is nothing, delete it
		if len( shapeList[ listIndex ] ) == 0:
			shapeList.pop( listIndex )
			
		# If the element is valid, separate it into a list of coordinate pairs
		else:		
			shapeList[ listIndex ] = shapeList[ listIndex ].strip( ",((" )
			listOf_shapesPoints.append( shapeList[ listIndex ].split( "," ) )
			listIndex += 1
			
	# Convert the list of coordinate pair strings into floats
	# Loop through each shape in the list 
	for shape in listOf_shapesPoints:
	
		# Loop thorugh the points in each shape
		for index in range( 0, len( shape ) ):
			
			# separate the x and y coordinates
			tempCoors = shape[ index ].split()
			
			#print( str( index ) + ": " + tempCoors[ 0 ] + ", " + tempCoors[ 1 ] )
			
			# Convert the coordaintes to floats 
			latitude = float( tempCoors[ 0 ] )
			longitude = float( tempCoors[ 1 ] )
			
			# Save the now converted coordinates
			shape[ index ] = ( latitude, longitude )
	
	# Save the actual shape file, leaving the holes in the listOf_shapesPoints list
	linearRing = listOf_shapesPoints.pop( 0 )
	
	try:
	# Create our polygon 
		if len( listOf_shapesPoints ) == 0:
			polygon = Polygon( linearRing )
		else:
			polygon = Polygon( linearRing, listOf_shapesPoints )
				
		# return our polygon
		return polygon.buffer( 0 )
		
	except ValueError:
		return Polygon( [(0,0), (0,0), (0,0 )] )
		
# Creates a multi-polygon object from our database's animal boundary information 
def create_multi_polygon( currentShape ):
	
	# Get rid of the cruft from the database string 
	shapeString = currentShape.strip( "'MULTIPOLYGON(((" ).strip( ")'," )
	polygonInfo = shapeString.split( "))" )
	listOfPolygons = []
		
	for index in range( 0, len( listOfPolygons ) ):
		listOfPolygons.append( create_polygon( polygonInfo[ index ] ) )
			
	multi_polygon = MultiPolygon( listOfPolygons )
	
	return multi_polygon
	
	
	

def create_shape( currentShape ):

	if currentShape is not None: 

		if "MULTIPOLYGON" in currentShape:
		
			return create_multi_polygon( currentShape )
			
		elif "POLYGON" in currentShape: 
		
			return create_polygon( currentShape )
			
		else:
			return Polygon( [(0,0), (0,0), (0,0)] )
			
			
			

def send_csv_to_drive( fileName ):

	print( 'begin file upload' )
	
	# Create google account authentication objects
	gauth = GoogleAuth('../../biodiversity_db_&_oauth/settings.yaml')
	
	'''
	print( 'client secrets 1' )
	
	if os.path.exists( 'biodiversity_db_&_oauth/credentials.txt' ):
		gauth.LoadCredentialsFile( 'biodiversity_db_&_oauth/credentials.txt' )
	
	if gauth.credentials is None:
		print( 'local webserver branch' )
		gauth.LocalWebserverAuth()
		
	elif gauth.access_token_expired:
		print( 'refresh branch' )
		gauth.Refresh()
		
	else:
		print( 'authorize branch' )
		gauth.Authorize()
	
	print( 'client secrets 2' )
		
	gauth.SaveCredentialsFile( 'biodiversity_db_&_oauth/credentials.txt' )
	'''
	
	drive = GoogleDrive( gauth )
	upload_csv = drive.CreateFile({ fileName: fileName + '.csv' })
	upload_csv.SetContentFile( fileName + '.csv' ) 
	upload_csv.Upload() 
	
	print( 'file uploaded' )

if __name__ == "__main__": 
	main()

#
