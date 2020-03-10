import csv
import os
import random
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

#from .biodiversity_image_scraper import image_scraper
from biodiversity_image_scraper import image_scraper

MASS = 16
BINOMIAL = 1
ANIMAL_TITLE = 0
ANIMAL_OBJECT = 1
ENDANGERED_STATUS = 5
ORDER = 9
NON_PREDATOR_ORDERS = [ "PROTURA", "EMBIOPTERA", "ZORAPTERA", "ISOPTERA", "MALLOPHAGA", "ANOPLURA", "HOMOPTERA", "SIPHONAPTERA" ] 

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    find_animal_images( 'mammal_info.csv', True, "animal_images" )

def find_animal_images( csv_name, upload_bool, dir_name ):
    # Open CSV file
    with open( csv_name ) as csv_file:

        print( BASE_DIR )

        animal_reader = csv.reader( csv_file, delimiter=',' )

        # Create a list with the animals from the csv
        animal_list = create_list_from_csv( animal_reader )

        # Sort the list of animals
        sort_results( animal_list )

        print( "animal list sorted" ) 

        # Create our list that contains exemplary animals 
        exemplary_animals = []

        
        # Find the largest animal
        exemplary_animals.append(("largest_animal", animal_list[ 0 ]))

        # Find the second largest animal 
        exemplary_animals.append(("second_largest_animal", animal_list[ 1 ] ))
        
        # Find the smallest animal
        exemplary_animals.append(("smallest_animal", animal_list[ len( animal_list)-1 ] ))

        # Find the second smallest animal
        exemplary_animals.append(("second_smallest_animal", animal_list[ len( animal_list ) - 2 ] ))

        # Find the largest predator
        exemplary_animals.append(("largest_predator", find_predator( 1, animal_list ) ))

        # Find the second largest predator
        exemplary_animals.append(( "second_largest_predator", find_predator( 2, animal_list )))

        # Find the largest past animal
        exemplary_animals.append(( "largest_past_animal", find_large_animal( 1, animal_list, True )))#find_large_animal(1, animal_list, True )))

        # Find the second largest past animal
        exemplary_animals.append(( "second_largest_past_animal", animal_list[ 3 ] ))

        # Find the largest historic predator

        # Find the second largest predator

        dobble_count = 28
        index = 0

        for dobble_image_count in range( 0, dobble_count ):

            exemplary_animals.append( ( "Dobble_" + str( dobble_image_count ), animal_list[ index ] ) )

            index += 1

            if index == len( animal_list ):
                
                index = 0

            
        # Initialize a list for the names of the images 
        image_names = []

        print( "saved animal info" )
        
        # Download the images for all of the animals we want 
        for animal in exemplary_animals:

            image_names.append( image_scraper( animal[ ANIMAL_OBJECT ][ BINOMIAL ], dir_name , animal[ ANIMAL_TITLE ] ))


        for image in image_names:
            print( image )
            
        # Upload the images to the Google drive 
        if upload_bool:
            upload_images( image_names )

                            
    

'''
Sorts the animal list from biggest to smallest
'''
def sort_results( animal_list ):
    quick_sort( animal_list, 0, len( animal_list ) - 1 )

def quick_sort( animal_list, low, high ):

    # Check if the list has not been sorted
    if low < high:

        # Find our partition
        partition_index = partition( animal_list, low, high )

        # Run quick sort on the lower end of the array
        quick_sort( animal_list, low, partition_index - 1)

        # Run quick sort on the higher end of the array
        quick_sort( animal_list, partition_index + 1, high )

def partition( animal_list, low, high ):

    # Initialize the partition index to the low
    partition_index = low - 1

    # Assign our pivot
    pivot = animal_list[ high ]

    # Loop through the section of the list
    for index in range( low, high ):

        # Check if the value at the current index is lower than the pivot
        if float( animal_list[ index ][ MASS ] ) >= float( pivot[ MASS ] ):

            # Increment our partition index
            partition_index += 1  

            # Swap the the current value with the partition index value
            temp = animal_list[ partition_index ]
            animal_list[ partition_index ] = animal_list[ index ]
            animal_list[ index ] = temp

    # Increment our partition index, so it's now the pivot index
    partition_index += 1
            
    # Swap our pivot with the value at one after the pivot index
    temp = animal_list[ partition_index ]
    animal_list[ partition_index ] = animal_list[ high ]
    animal_list[ high ] = temp 

    # Return the pivot index
    return partition_index
        
    

def create_list_from_csv( csv_file ):

    # Initialize a list
    animal_list = []

    # Make sure to skip the first row, as it is the categories
    looking_at_animals = False
    
    # Run through the CSV file
    for animal in csv_file:

        if looking_at_animals:
            
            # Add the current row from the csv file to the list
            animal_list.append( animal )

        else:

            # Since we skipped the categories, we are now looking at the actual animals
            looking_at_animals = True

    # Return the list
    return animal_list

def find_predator( placement, animal_list ):

    placement_counter = placement
    
    # Loop through the list
    for animal in animal_list:

        if animal[ 0 ] != "historic": 

            # Check if the animal is a predator
            if animal[ ORDER ] not in NON_PREDATOR_ORDERS:

                # Subtrack from our placement counter
                placement_counter -= 1

                # Check if our placement counter is zero
                if placement_counter == 0:
                
                    # If so, return this animal
                    return animal 

    # If no predators were found, return the largest animal
    return animal_list[ 0 ]

def find_large_animal( placement, animal_list, historic=False ):

    placement_counter = placement
    found_animal = animal_list[ 0 ] 

    for animal in animal_list:

        if placement_counter != 0:

            # Check if  we're searching or historic animals
            if historic:
                
                # Check if the animal is historic
                if animal[ 0 ] == "historic" or animal[5] == "Extinct" :

                    # Save it to our last animal
                    found_animal = animal

            # Otherwise, assume that we're are searching for current animals
            else:

                # Check if the animal is historic
                if animal[ 0 ] != "historic":

                    # Save it to our last animal
                    found_animal = animal
                    
        placement_counter -= 1

    return found_animal
            

def upload_images( images ):

    # connect to google drive 
    gauth = GoogleAuth('../../biodiversity_db_&_oauth/settings.yaml' )
    drive = GoogleDrive( gauth )

    if os.path.exists( 'credentials.txt' ):
        gauth.LoadCredentialsFile( 'credentials.txt' )

    if gauth.credentials is None:
        print( 'local webserver branch' )
        gauth.LocalWebserverAuth()
        gauth.SaveCredentialsFile( 'credentials.txt' )

    elif gauth.access_token_expired:
        print( 'refresh branch' )
        gauth.Refresh()

    else:
        print( 'authorize branch' )
        gauth.Authorize()

    print( "after authorization" )

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
    
    # Loop through the images
    for image_name in images: 
        upload_image = drive.CreateFile( {'title': image_name, 'parents': [{'id': target_folder_id }]})
        
        #upload_image.SetContentFile( "python_scripts/biodiversity/animal_images/" + image_name )

        print( image_name )
        
        upload_image.SetContentFile( "animal_images/" + image_name )
        
        upload_image.Upload()

if __name__ == "__main__":
    main()
