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

# constant for testing database executions 
ROWS_TO_ACCESS = 1
	
# The size of the area that we want to search for 
# 1 about equals 70 miles  (69.4)
SEARCH_RADIUS = 0.1

def main():

        db_path = ""
        
        # Our boolean that maintains the main loop 
        getting_info = True

        descriptors = get_descriptors( db_path )
        animal_boundaries = []
        animal_info = []

        print( "beginning local db read" )
        get_mammal_db( db_path, animal_info, animal_boundaries )                                
        print( "finished reading database" )

        while getting_info:

                animals_within_boundaries = []
                print( "Enter latitude and longitude (comma separated) or \"exit\" to exit: " )
                response = input()
                if response.lower() == "exit":
                        getting_info = False

                elif response.lower() == "search":

                        # Find the index of the animal we want to find
                        print( "Enter the binomial of the animal: " ) 
                        response = input()
                        animal_index = find_animal_index_by_name( response, animal_info )

                        if animal_index == 0:
                                print( "could not find animal" )
                                continue
                        
                        # Compare it to a lat long
                        print( "Enter a latitude and longitude" )
                        coordinates = input()
                        coordinates = coordinates.split( "," )
                        
                        latitude = float( coordinates[ 0 ] )
                        longitude = float( coordinates[ 1 ] )

                        if animal_index != 0:

                                print( "animla at: " + str( animal_index ) )
                                # Print if it was within those coordinates
                                search_result = checkCoordinates_in_animalInfo( longitude, latitude, animal_boundaries[ animal_index ], SEARCH_RADIUS )

                                '''
 # create a polygon object originating from the latitude and longitude
        origin_point = Point( latitude, longitude )
	
        # Create a circle that will be where we search for animal habitats
        search_area = origin_point.buffer( search_radius )
                                '''
                                
                                if search_result:
                                	print( "animal was on that" )
                                else:
                                	print( "it was not there" )
                                        
                                origin_point = Point( longitude, latitude )
                                search_area = origin_point.buffer( SEARCH_RADIUS )

                                print( "boundary count: " + str( len( animal_boundaries[ animal_index ] )) )
                                
                                for area in animal_boundaries[ animal_index ]:
                                        print( "distance: " + str( area.distance( search_area )) )
                                        
                                # Print the bounds of the animal
                                #print( animal_boundaries[ animal_index ].bounds() )
                        else:
                                print( "Could not find animal" )
                                
                else:
                                
                        try:
                                response = response.split( "," )
                        
                                latitude = float( response[ 0 ] )
                                longitude = float( response[ 1 ] )
                                find_animals( descriptors, animal_info, animal_boundaries, longitude, latitude )

                        except:
                                print( "not valid input" )
	
	
# end main 	

def find_animals_script( latitude, longitude ):

        db_path = "biodiversity_db_&_oauth/"

        descriptors = get_descriptors( db_path )
        animal_boundaries = []
        animal_info = []

        print( "beginning local db read" )
        get_animal_db( db_path, animal_info, animal_boundaries )                                
        print( "finished reading database" )

        return find_animals( descriptors, animal_info, animal_boundaries, longitude, latitude )
                        





def find_animals( descriptors, animal_info, animal_boundaries, longitude, latitude ):

        animals_within_boundaries = []
        
        try:
                for index in range( 0, len( animal_boundaries )):

                        if checkCoordinates_in_animalInfo( longitude, latitude, animal_boundaries[ index ], SEARCH_RADIUS ):
                                animals_within_boundaries.append( animal_info[ index ] )
                                
                if len( animals_within_boundaries ) == 0:
                        print( "There were no mammals in that area" )
                else:
                        filename = write_mammal_info_to_csv( animals_within_boundaries, descriptors, latitude, longitude )
                        #send_csv_to_drive( filename )
                        #display_mammal_information( animals_within_boundaries, descriptors )
                        print( "number of animals" )
                        print( len( animals_within_boundaries ) )
			
                        return filename + '.csv'
                
        except ValueError:
                print( "Please input a valid latitude and longitude or \"Exit\" " )	




                
def get_mammal_db( path, animal_info, animal_boundaries ):
        
        with open( path + "biodiversity_mammal_db.csv" ) as csvFile:
                csv.field_size_limit( sys.maxsize )
                curr_reader = csv.reader( csvFile )

                index = 0

                for row in curr_reader:
                        
                        if index == 0:
                                descriptors = row
                        else:
                                animal_info.append( row )

                                append_shape( animal_boundaries, animal_info[ index - 1 ][ 17 ] )
                                #animal_boundaries.append( create_shape( animal_info[ index - 1 ][ 17 ]))

                        index += 1

                        if index % 1000 == 0:
                                print( "read in " + str( index ) + " current animals" )

        with open( path + "biodiversity_hist_db.csv" ) as csvFile:
                hist_reader = csv.reader( csvFile )

                index = 0

                for row in hist_reader:

                        if index != 0:
                                animal_info.append( create_hist_animal( row ))

                                append_shape( animal_boundaries, animal_info[ index - 1 ][ 17 ] )
                                #animal_boundaries.append( create_shape( animal_info[ index - 1 ][17] ))

                        index += 1
                        
                        if index % 100 == 0:
                                print( "read in " + str( index ) + " historic animals" )
                        


def get_descriptors( path ):
        with open( path + "biodiversity_mammal_db.csv" ) as csvFile:
                curr_reader = csv.reader( csvFile )

                for row in curr_reader:
                        return row

        



def find_animal_index_by_name( binomial, animal_info ):

        index = 0
        
        for animal in animal_info:

                animal = list( animal )
                if animal[ 1 ].lower() == binomial.lower():
                        return index

                index += 1

        return 0 

                                

                
# Check if an animal's habitat area is within the area we're searching 
def checkCoordinates_in_animalInfo( latitude, longitude, animal_boundary, search_radius ):
	
        # create a polygon object originating from the latitude and longitude
        origin_point = Point( latitude, longitude )
	
        # Create a circle that will be where we search for animal habitats
        search_area = origin_point.buffer( search_radius )

        # Turn this circle into a polygon object that can be used to check if it
        # intersects with an animal's polygon object that represents its habitat
        search_polygon = Polygon( list( search_area.exterior.coords ) )

        # Otherwise, check if our search area intersects with the animal's habitat
        for boundary in animal_boundary:
                
                # Check if any of the animal boundaries intersect with the search area
                if search_polygon.intersects( boundary ) and boundary.is_valid:

                        # If one does intersect, return true 
                        return True

        # If none of the boundaries intersected, then return false 
        return False

        #return search_polygon.intersects( animal_boundary )



        

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
        file_wo_extension = "mammal_info" #_" + str( latitude ) + '_' + str( longitude )
        file_name = file_wo_extension + ".csv"
	
        # Create a CSV file to write to 
        with open( file_name, mode='w' ) as csv_file: 
                writer = csv.writer( csv_file )
		
                # Write the latitude and longitude to the CSV
                #writer.writerow( [ latitude, longitude ] )
		
                # Delete the 17th column in the descriptors 
                #headers = list( descriptors )
                #headers.pop( 17 )	
			
                # Write the descriptors/headers to the file 
                #writer.writerow( headers )
		
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
def create_polygon( currentShape, multi ):

        listOf_shapesPoints = []
        # Separate our list of coordinates into the shell and the holes
        shapeList = currentShape.strip( "('POLYGON((" ).strip( "))',)" ).split( ")" )

        # Delete all of the empty elements in the list
        listIndex = 0
        for	i in range( 0, len( shapeList ) ):

                # If an element in the list is nothing, delete it
                if len( shapeList[ listIndex ] ) == 0:
                        shapeList.pop( listIndex )

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
                if len( listOf_shapesPoints ) == 0:
                        polygon = Polygon( linearRing )

                else:
                        polygon = Polygon( linearRing, listOf_shapesPoints )

                return polygon.buffer( 0 )

        except ValueError:
                return Polygon( [(0,0), (0,0), (0,0 )] )
		
# Creates a multi-polygon object from our database's animal boundary information 
def create_multi_polygon( currentShape ):
	
	# Get rid of the cruft from the database string
        shapeString = currentShape.strip( "'MULTIPOLYGON(((" ).strip( ")'," )
        polygonInfo = shapeString.split( "))" )
        listOfPolygons = []

        for index in range( 0, len( polygonInfo ) ):
                gon_guy = create_polygon( polygonInfo[ index ], True )
                
                listOfPolygons.append( gon_guy )
                
        return listOfPolygons
			
	#multi_polygon = MultiPolygon( listOfPolygons )
	
	#return multi_polygon

	
	
'''
def create_shape( currentShape ):

	if currentShape is not None: 

		if "MULTIPOLYGON" in currentShape:
		
			return create_multi_polygon( currentShape )
			
		elif "POLYGON" in currentShape: 
		
			return create_polygon( currentShape )
			
		else:
			return Polygon( [(0,0), (0,0), (0,0)] )
'''


def append_shape( animal_boundaries, currentShape ):

        if currentShape is not None:

                if "MULTIPOLYGON" in currentShape:
                        animal_boundaries.append( create_multi_polygon( currentShape ))

                elif "POLYGON" in currentShape:
                        animal_boundaries.append([ create_polygon( currentShape, False ) ])

                else:
                        animal_boundaries.append([ Polygon( [(0,0), (0,0), (0,0)] ) ])

        else:
                animal_boundaries.append([ Polygon( [(0,0), (0,0), (0,0)] ) ])
			
			
			

def send_csv_to_drive( fileName ):

        print( 'begin file upload' )
        # Create google account authentication objects
        gauth = GoogleAuth('../../biodiversity_db_&_oauth/settings.yaml')

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

        drive = GoogleDrive( gauth )

        ''' Find the name of the folder we want to upload to '''
        # Define the folder we want to upload to
        target_folder_name = 'slideInfo'
        target_folder_id = ''

        # Find the list of all of the files in the google drive
        file_list = drive.ListFile({ 'q': "'root' in parents and trashed=false"}).GetList()

        # Loop through all of the files in the
        for file_object in file_list:

                # Check if the current one is our target
                if file_object[ 'title' ] == target_folder_name:

                        # Save the folder id
                        target_folder_id = file_object[ 'id' ]

        print( "folder id: " + target_folder_id )

        upload_csv = drive.CreateFile({ fileName: fileName + '.csv', 'parents': [{'id': target_folder_id }] })
        upload_csv.SetContentFile( fileName + '.csv' )
        upload_csv.Upload()

        print( 'file uploaded' )

def create_hist_animal( animal ):

        # Create the animal template that is the same size as the regular animal
        info_list = [None] * 18

        # Save the historic animal info into the template
        # Set the id to say that this is a historic animal
        info_list[ 0 ] = "historic" 
        # Binomial 
        info_list[ 1 ] = animal[ 0 ]
        # Common name 
        info_list[ 13 ] = animal[ 1 ]
        # Wiki Link 
        info_list[ 14 ] = animal[ 2 ]
        # Description 
        info_list[ 15 ] = animal[ 3 ]
        # Boundaries
        info_list[ 17 ] = animal[ 4 ]
        # Mass
        info_list[ 16 ] = animal[ 5 ]

        # Return the animal list
        return info_list
        
if __name__ == "__main__": 
	main()

#
