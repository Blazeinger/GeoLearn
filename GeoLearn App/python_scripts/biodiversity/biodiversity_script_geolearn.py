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

try:
    from biodiversity_db_scanner import biodiversity_db_generator
    from biodiversity_results_sorter import basic_image_finder, advanced_image_finder
    from enviro_log import enviro_logger
 
except:
    from .biodiversity_db_scanner import biodiversity_db_generator
    from .biodiversity_results_sorter import write_csvs
    from .enviro_log import enviro_logger

# constant for testing database executions 
ROWS_TO_ACCESS = 1
	
# The size of the area that we want to search for 
# 1 about equals 70 miles  (69.4)
SEARCH_RADIUS = 0.5

# The path to where the file is, biodiversity
CURR_DIR = os.path.dirname(os.path.realpath(__file__))

# The path to the GeoLearn App directory
BASE_DIR = CURR_DIR.replace( "/python_scripts/biodiversity", "" )

# Logger to write commandline output to a text file for server testing
logger = enviro_logger()

def main():

    # Path to the csv databases 
    db_path = ""
        
    # Our boolean that maintains the main loop 
    getting_info = True

    # Initialize lists that will contain the animal information
    descriptors = []
    animal_boundaries = []
    animal_info = []

    # Retrieve the database information from the local CSV databases
    logger.log( "beginning local db read" )
    get_mammal_db( db_path, animal_info, animal_boundaries )                           
    logger.log( "finished reading database" )

    # While running this as a main, allow the user to keep inputting values
    while getting_info:

        # Create an empty list that will contain all the animals close to the search area
        animals_within_boundaries = []
        
        # As the user for a latitude and longitude
        logger.log( "Enter latitude and longitude (comma separated) or \"exit\" to exit: " )
        response = input()
        
        # Check if the user wants to exit the program 
        if response.lower() == "exit":
            getting_info = False
        
        # Check user wants to search for a specific animal for testing purposes
        elif response.lower() == "search":

            # Ask the user for the animal they want to search for
            logger.log( "Enter the binomial of the animal: " ) 
            response = input()
            
            # Find the index of the animal we want to find
            animal_index = find_animal_index_by_name( response, animal_info )

            # If 0 is returned as the animal index, there was no match for the input binomial 
            if animal_index == 0:
                logger.log( "could not find animal" )
                continue

            # Otherwise, we have the index for the animal we're searching for
            if animal_index != 0:

                # Ask the user for coordinates
                logger.log( "Enter a latitude and longitude" )
                coordinates = input()
                coordinates = coordinates.split( "," )
                        
                # Convert the coordinates to workable values
                longitude = float( coordinates[ 1 ] )
                latitude = float( coordinates[ 0 ] )

                # Print the index the animal was found at in the database
                logger.log( "animal at index: " + str( animal_index ) )
                
                # Check if the animal we're searching for is within the coordinate we've searched for
                search_result = checkCoordinates_in_animalInfo( longitude, latitude, animal_boundaries[ animal_index ], SEARCH_RADIUS )
                                
                # Tell the user if the animal was found in that location or not 
                if not search_result:
                    logger.log( "it was not there" )
                    
                else:
                    logger.log( "animal was on that" )
                    
                # Manually create a search area polygon that we can use to find the distance between the search area and the animal boundary
                origin_point = Point( longitude, latitude )
                # Make the search area radius the same as the regular search radius
                search_area = origin_point.buffer( SEARCH_RADIUS )

                # Let the user know how many boundaries the animal has 
                logger.log( "boundary count: " + str( len( animal_boundaries[ animal_index ] )) )
                                
                # For every boundary that the animal has, print the distance between it and the search area
                # Loop through each individual boundary and print the values
                for boundary in animal_boundaries[ animal_index ]:
                    logger.log( "        {}".format( list(boundary.bounds) ))
                    logger.log( "    " + str( boundary.distance( search_area )) )
                    
            # Otherwise, the animal could not be found
            else:
                logger.log( "Could not find animal" )

        # Check if the user wants to check the historic animal information 
        elif response.lower() == "hist" or response.lower() == "hist full": 
                
            # Check if the user wants the full historic information
            if response.lower() == "hist full":
                full_output = True
                
            # Otherwise, assume they want only the historic info around the search area
            else:
                full_output = False
                        
            # Compare it to a lat long
            logger.log( "Enter a latitude and longitude" )
            coordinates = input()
            coordinates = coordinates.split( "," )
                        
            latitude = float( coordinates[ 0 ] )
            longitude = float( coordinates[ 1 ] )
                        
            # create a polygon object originating from the latitude and longitude
            origin_point = Point( longitude, latitude )
	
            # Create a circle that will be where we search for animal habitats
            search_area = origin_point.buffer( SEARCH_RADIUS )

            # Turn this circle into a polygon object that can be used to check if it
            # intersects with an animal's polygon object that represents its habitat
            search_polygon = Polygon( list( search_area.exterior.coords ) )

            # Loop through all the animals
            for index in range( len( animal_info )):
                                
                # Make sure they're all historic 
                if animal_info[ index ][0] == "historic":
                                
                    # Let the user know the name of the animal 
                    logger.log( "{} bounds: ".format( animal_info[ index ][1] ) )
                                        
                    # Loop through the boundaries for the animal 
                    for boundary in animal_boundaries[ index ]:
                                        
                        # Print the distance between the search area and the boundary if it's less than 30 or if we want all the information
                        if boundary.distance( search_area ) < 30 or full_output:
                                                
                            logger.log( "        {}".format( list(boundary.bounds) ))
                            logger.log( "    " + str( boundary.distance( search_polygon )) )
                            
        elif response.lower() == "sort":
            
            logger.log( "(b)eginner or (a)dvanced?: " )
            difficulty = input()
            
            if difficulty.lower() == 'b' or difficulty.lower() == "beginner":
                basic_image_finder( False, 'animal_images', 'mammal_info.csv' )
                
            elif difficulty.lower() == 'a' or difficulty.lower() == 'advanced':
                advanced_image_finder( False, 'animal_images', 'mammal_info.csv' )
            
            else:
                logger.log( "invalid difficulty" )
            
        
        # Otherwise, assume we're running normally and checking animals within the search area
        else:
            
            # Be able to take in invalid input without crashing when running as main 
            try:
            
                # Take the users' response and convert it to latitude and longitude
                response = response.split( "," )
                        
                latitude = float( response[ 0 ] )
                longitude = float( response[ 1 ] )
                
                # Determine the difficulty of the slideshow, so we know which google drive folder to upload to
                difficulty = input( "(b)eginner or (a)dvanced?: " )
                
                # Change the target google drive directory based on input and let the user know
                if difficulty.lower() == "b":
                    target_dir = "slideInfo_BioBasic"
                    logger.log( "beginner presentation selected" )
                    
                elif difficulty.lower() == "a":
                    target_dir = "slideInfo_BioAdv"
                    logger.log( "advanced presentation selected" )
                    
                # If invalid input, do the beginner presentation by default
                else:
                    target_dir = "slideInfo_BioBasic" 
                    logger.log( "default selected, basic" )
                    
                logger.log( find_animals( descriptors, animal_info, animal_boundaries, longitude, latitude, target_dir ) )

            except:
                logger.log( "not valid input" )
	
	
# end main

def find_animals_script( latitude, longitude, target_dir ):

    db_path = "" #python_scripts/biodiversity/"

    descriptors = []
    animal_boundaries = []
    animal_info = []

    logger.log( "beginning local db read" )
    get_mammal_db( db_path, animal_info, animal_boundaries )                                
    logger.log( "finished reading database" )

    return find_animals( descriptors, animal_info, animal_boundaries, longitude, latitude, target_dir )
                        





def find_animals( descriptors, animal_info, animal_boundaries, longitude, latitude, target_dir ):

    animals_within_boundaries = []
        
    try:

        # Compare all of the animals' habitats to our search area
        for index in range( 0, len( animal_boundaries )):

            if checkCoordinates_in_animalInfo( longitude, latitude, animal_boundaries[ index ], SEARCH_RADIUS ):
                animals_within_boundaries.append( animal_info[ index ] )
                                
            if index % 500 == 0:
                logger.log( str(index) + " animals tested" )

        # Check if we couldn't find any animals in our search area
        if len( animals_within_boundaries ) == 0:
            logger.log( "There were no mammals in that area" )

        # If animals were found, write them to the csv
        else:
            filename = write_mammal_info_to_csv( animals_within_boundaries, descriptors, latitude, longitude )
            
            if __name__ != "__main__":
            	send_csv_to_drive( BASE_DIR + "/" + filename, filename, target_dir )
            #display_mammal_information( animals_within_boundaries, descriptors )
            logger.log( "number of animals" )
            logger.log( len( animals_within_boundaries ) )
            
            logger.log( filename )
            assert filename != None
            
            logger.log( "done" )
			
            return BASE_DIR + "/" + filename + ".csv"
                
    except ValueError:
        logger.log( "Please input a valid latitude and longitude or \"Exit\" " )	




                
def get_mammal_db( path, animal_info, animal_boundaries ):

    if __name__ == "__main__":
        trait_path = "/"
        db_path = "/"
        
    else:
        trait_path = "/"
        db_path = "/"
    
    basest_dir = BASE_DIR
    
    # Check if the database exists
    if os.path.exists( basest_dir + db_path + 'biodiversity_mammal_db.csv' ) and os.path.exists( basest_dir + db_path + 'biodiversity_hist_db.csv' ):

        logger.log( "databases already exist" )
        
    else:
    
        logger.log( "generating databases" )
        
        generator = biodiversity_db_generator()
        generator.generate_db_csv( read_path=trait_path, write_path=db_path, server_run=True )
        generator = ""

    with open( basest_dir + db_path + "biodiversity_mammal_db.csv", encoding="utf8" ) as csvFile:
        csv.field_size_limit( sys.maxsize )
        curr_reader = csv.reader( csvFile )

        index = 0

        for row in curr_reader:
                        
            if index == 0:
                descriptors = row
            else:
                animal_info.append( row )

                append_shape( animal_boundaries, animal_info[ index - 1 ][ 17 ] )

            index += 1

            if index % 1000 == 0:
                logger.log( "read in " + str( index ) + " current animals" )

                
    with open( basest_dir + db_path + "/biodiversity_hist_db.csv", encoding="utf8" ) as csvFile:
        hist_reader = csv.reader( csvFile )
                
        # Skip the categories bit
        next( hist_reader )

        for row in hist_reader:
                
            animal_info.append( create_hist_animal( row ))

            append_shape( animal_boundaries, animal_info[ index - 1][ 17 ] )
            #animal_boundaries.append( create_shape( animal_info[ index - 1 ][17] ))

            index += 1
                        
            if index % 100 == 0:
                
                logger.log( "read in " + str( index ) + " historic animals" )

        
    

    
                        

def get_descriptors( path ):
    with open( path + "biodiversity_mammal_db.csv", encoding="utf8" ) as csvFile:
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
        if search_polygon.intersects( boundary ):

            # If one does intersect, return true 
            return True

    # If none of the boundaries intersected, then return false 
    return False



        

# Print the animal's information to the commandline 
def display_mammal_information( listOfMammals, descriptors ):

    for x in listOfMammals:
        for index in range( 0, len( x )):
            if index != 17:	
            	logger.log( " - " + descriptors[ index ], end= ": " )
            	logger.log( x[ index ] )
		
    logger.log( "\n====================\n" )



                

# Write our found animals' information to a CSV file 
def write_mammal_info_to_csv( listOfMammals, descriptors, latitude, longitude ):

    # Variables
    now = datetime.now()
    list_of_mammals_cleaned = [];

    # Create CSV file name
    # Add the date and time to ensure that the file names are unique
    file_wo_extension = "mammal_info" #_" + str( latitude ) + '_' + str( longitude )

    file_name = BASE_DIR + "/" + file_wo_extension + ".csv" 

    with open( file_name, mode='w', encoding="utf8" ) as csv_file:
        #os.chmod(file_name, 0o777)
        writer = csv.writer( csv_file )

        # Loop through each animal we found
        for animal in listOfMammals:

            # Create a list of the animal's info
            mammal_info = list( animal )

            # Delete the 17th index, the shape files
            mammal_info.pop( 17 )

            # Write the information to the row in the CSV
            writer.writerow( mammal_info )

    # Print to the user that the CSV file has been printed
    logger.log( "done writing to CSV file" )
    
    assert file_name != None
    assert file_wo_extension != None

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

            #logger.log( str( index ) + ": " + tempCoors[ 0 ] + ", " + tempCoors[ 1 ] )

            # Convert the coordaintes to floats
            latitude = float( tempCoors[ 0 ] )
            longitude = float( tempCoors[ 1 ] )

            # Save the now converted coordinates
            shape[ index ] = ( latitude, longitude )

    # Save the actual shape file, leaving the holes in the listOf_shapesPoints list
    linearRing = listOf_shapesPoints.pop( 0 )

    try:
        if len( listOf_shapesPoints ) == 0:
                
            # Sometimes, the area the animal lives is a point
            if len( linearRing ) == 2:
                linearRing.append( linearRing[ 0 ] )
                                
            polygon = Polygon( linearRing )

        else:
                        
            polygon = Polygon( linearRing, listOf_shapesPoints )
            
        return polygon

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
			
			
			

def send_csv_to_drive( fileName, fileAlias, target_dir="slideInfo_BioBasic" ):

    logger.log( 'begin file upload' )
    
    client_secrets_path = BASE_DIR + "/client_secrets.json" 
    credentials_path = BASE_DIR + "/credentials.txt"
    
    GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = client_secrets_path
        
    # Create google account authentication objects
    gauth = GoogleAuth()

    logger.log( 'Looking for credentials' )
    
    if os.path.exists( credentials_path ):
        logger.log( 'found a credentials' )
        gauth.LoadCredentialsFile( credentials_path )

    if gauth.credentials is None:# or gauth.access_token_expired:
        logger.log( 'local connect to website' )
        gauth.LocalWebserverAuth()
        gauth.SaveCredentialsFile( credentials_path )

    elif gauth.access_token_expired:
        logger.log( 'refresh branch' )        
        gauth.Refresh()

    else:
        logger.log( 'authorize branch' )
        gauth.Authorize()

    logger.log( 'creating connection to google drive' )

    gauth.SaveCredentialsFile( credentials_path )
    

    drive = GoogleDrive( gauth )
    
    logger.log( 'connection established' )

    ''' Find the name of the folder we want to upload to '''
    # Define the folder we want to upload to
    target_folder_name = target_dir
    target_folder_id = ''

    logger.log( 'finding drive folder: ' + target_dir )

    folder_not_found = True
    
    while( folder_not_found ):

        # Find the list of all of the files in the google drive
        file_list = drive.ListFile({ 'q': "'root' in parents and trashed=false"}).GetList()

        # Loop through all of the files in the
        for file_object in file_list:

            # Check if the current one is our target
            if file_object[ 'title' ] == target_folder_name:

                # Save the folder id
                target_folder_id = file_object[ 'id' ]
                
                # Exit the while loop
                folder_not_found = False
                
        # Check if the folder was found
        if target_folder_id == '':
        
            logger.log( 'folder not found. Creating one' )
            
            # Create the folder we want
            folder = drive.CreateFile( 
                {'title': target_folder_name, 
                'mimeType': 'application/vnd.google-apps.folder' } )
            
            # Upload the folder to the drive 
            folder.Upload()
            
            # The loop will go again, but now it will find the folder
            

    logger.log( "folder found. id: " + target_folder_id )

    upload_csv = drive.CreateFile({ 'title': fileAlias + '.csv', 'parents': [{'id': target_folder_id }] })
    upload_csv.SetContentFile( fileName + '.csv' )
    upload_csv.Upload()

    logger.log( 'file uploaded' )




    

def create_hist_animal( animal ):

    # Create the animal template that is the same size as the regular animal
    info_list = [None] * 24

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
        
    ''' The historic database has these swapped, I guess'''
    # Boundaries
    info_list[ 17 ] = animal[ 4 ]
    # Mass
    info_list[ 16 ] = animal[ 5 ]
        
    ''' Some historic animals didn't have diet data''' 
        
    try:
        # Plant diet
        info_list[20] = animal[6]
        # Vertebrate Diet
        info_list[21] = animal[7]
        # Invertebate Diet
        info_list[22] = animal[8]
        # Return the animal list
        info_list[23] = animal[9]
    except IndexError:
                
        # Plant diet
        info_list[20] = 0
        # Vertebrate Diet
        info_list[21] = 0
        # Invertebate Diet
        info_list[22] = 0
        # Return the animal list
        info_list[23] = "no data"
        
    return info_list
        
if __name__ == "__main__": 
    main()

#
