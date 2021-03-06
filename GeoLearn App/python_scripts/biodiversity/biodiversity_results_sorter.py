import csv
import os
import random
import sys
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

try:
    from biodiversity_image_scraper import images_scraper
    from enviro_log import enviro_logger
except:
    from .biodiversity_image_scraper import images_scraper
    from .enviro_log import enviro_logger

MASS = 16
BINOMIAL = 1
ANIMAL_TITLE = 0
ANIMAL_OBJECT = 1
ENDANGERED_STATUS = 5
ORDER = 9
DIET = 22
NON_PREDATOR_ORDERS = [ "PROTURA", "EMBIOPTERA", "ZORAPTERA", "ISOPTERA", "MALLOPHAGA", "ANOPLURA", "HOMOPTERA", "SIPHONAPTERA" ] 

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
basest_dir = BASE_DIR.replace( "python_scripts", "" )
CURR_DIR = os.path.dirname(os.path.realpath(__file__))

logger = enviro_logger()

def main():

    upload_bool = sys.argv[1]
    dir_name = sys.argv[2] 
    csv_name = sys.argv[3]
    difficulty = sys.argv[4]

    if upload_bool == "True":
        upload = True
    else:
        upload = False

    if difficulty == "beginner":
        logger.log( "beginner results chosen" )
        basic_image_finder( upload, dir_name, csv_name )
        
    elif difficulty == "advanced":
        logger.log( "advanced results chosen" )
        advanced_image_finder( upload, dir_name, csv_name )
    
def basic_image_finder( upload_bool, dir_name, csv_name="mammal_info" ):

    if csv_name == None:
        csv_name = "mammal_info" 

    # Open CSV file
    with open( csv_name, encoding='utf8' ) as csv_file:

        animal_reader = csv.reader( csv_file, delimiter=',' )

        # Create a list with the animals from the csv
        animal_list = create_list_from_csv( animal_reader )

        # Sort the list of animals
        sort_results( animal_list )

        logger.log( "animal list sorted" ) 

        # Create our list that contains exemplary animals 
        exemplary_animals = []

        image_titles = [ "largest_animal", "second_largest_animal", "smallest_animal", "second_smallest_animal", "largest_predator", "second_largest_predator", "largest_past_animal", "second_largest_past_animal", "large_herbivore", "second_largest_herbivore",
"largest_non-predator", "second_largest_non-predator", "largest_historic_predator", "second_largest_historic_predator", 
"largest_historic_non-predator", "second_largest_historic_non-predator" ]
      
        # Find the largest animal
        exemplary_animals.append(( image_titles[0], find_large_animal( 1, animal_list, exemplary_animals ) ))

        # Find the second largest animal 
        exemplary_animals.append(( image_titles[1], find_large_animal( 1, animal_list, exemplary_animals ) ))
        
        
        # Find the smallest animal
        exemplary_animals.append(( image_titles[2], find_smallest_animal( 1, animal_list, exemplary_animals ) ))

        # Find the second smallest animal
        exemplary_animals.append(( image_titles[3], find_smallest_animal( 1, animal_list, exemplary_animals ) ))
        

        # Find the largest predator
        exemplary_animals.append(( image_titles[4], find_predator( 1, animal_list, exemplary_animals ) ))

        # Find the second largest predator
        exemplary_animals.append(( image_titles[5], find_predator( 1, animal_list, exemplary_animals ) ))
        

        # Find the largest past animal
        exemplary_animals.append(( image_titles[6], find_large_animal( 1, animal_list, exemplary_animals, True )))#find_large_animal(1, animal_list, True )))

        # Find the second largest past animal
        exemplary_animals.append(( image_titles[7], find_large_animal( 2, animal_list, exemplary_animals, True ) ))
        
        
        # Find the largest herbivore
        exemplary_animals.append(( image_titles[8], find_herbivore( 1, animal_list, exemplary_animals ) ))
        
        # Find the second largest herbivore
        exemplary_animals.append(( image_titles[9], find_herbivore( 1, animal_list, exemplary_animals ) ))
        
        
        # Find the largest non-predator
        exemplary_animals.append(( image_titles[10], find_non_predator( 1, animal_list, exemplary_animals ) ))
        
        # Find the second largets non-predator
        exemplary_animals.append(( image_titles[11], find_non_predator( 1, animal_list, exemplary_animals ) ))
        
        
        # Find the largest historic predator 
        exemplary_animals.append(( image_titles[12], find_predator( 1, animal_list, exemplary_animals, True ) ))
        
        # Find the second largest historic predator
        exemplary_animals.append(( image_titles[13], find_predator( 2, animal_list, exemplary_animals, True ) ))
        
        
        # Find the largest historic non-predator 
        exemplary_animals.append(( image_titles[14], find_non_predator( 1, animal_list, exemplary_animals, True ) ))
        
        # Find the second largest historic non-predator
        exemplary_animals.append(( image_titles[15], find_non_predator( 2, animal_list, exemplary_animals, True ) ))
        
        
        # Find 3 more herbivores 
        for placement in range( 3, 6 ):
        
            found_animal = find_herbivore( 1, animal_list, exemplary_animals )
            
            if found_animal:
                exemplary_animals.append(( "large_herbivores_" + str( placement - 2), found_animal ))
            
                image_titles.append( "large_herbivores_" + str( placement - 2) )
                
                
        # Find 3 more predators
        for placement in range( 3, 6 ):
        
            found_animal = find_predator( 1, animal_list, exemplary_animals )
            
            if found_animal:
            
                exemplary_animals.append(( "large_predators_" + str( placement - 2), found_animal ))
                
                image_titles.append( "large_predators_" + str( placement - 2) )
                
            
        # Find 6 historic animals
        for placement in range( 3, 9 ):
        
            found_animal = find_large_animal( placement, animal_list, exemplary_animals, True )
            
            if found_animal:
            
                exemplary_animals.append(( "historic_" + str( placement - 2 ), found_animal ))
                
                image_titles.append( "historic_" + str( placement - 2 ) )
            
        

        dobble_count = 28
        exemplary_animals.extend( find_dobble_images( dobble_count, animal_list, image_titles ) )
            
        # Initialize a list for the names of the images 
        image_names = []
        
        write_csvs( "sorted_mammal_info.csv", "chosen_mammals_info.csv", animal_list, exemplary_animals )        
        
        
        
        # Upload the images to the Google drive 
        
        if upload_bool:
        
            images_scraper( "chosen_mammals_info.csv" )
            upload_files( image_titles, "chosen_mammals_info.csv" )
            
        return "chosen_mammals_info.csv"
        




            
        
def advanced_image_finder( upload_bool, dir_name, csv_name="mammal_info" ):
    
    if csv_name == None:
        csv_name = "mammal_info" 

    # Open CSV file
    with open( csv_name, encoding='utf8' ) as csv_file:

        animal_reader = csv.reader( csv_file, delimiter=',' )

        # Create a list with the animals from the csv
        animal_list = create_list_from_csv( animal_reader )

    # Sort the list of animals
    sort_results( animal_list )

    logger.log( "animal list sorted" )

    chosen_animals = []

    image_titles = [ "largest_herbivore",
                     "second_largest_herbivore",
                     "largest_predator",
                     "second_largest_predator" ]

    # Find the largest herbivores
    chosen_animals.append(( image_titles[0], find_herbivore( 1, animal_list, chosen_animals ) ))
        
    # Find the second largest herbivore
    chosen_animals.append(( image_titles[1], find_herbivore( 1, animal_list, chosen_animals ) ))
    
    # Find the largest predator
    chosen_animals.append(( image_titles[2], find_predator( 1, animal_list, chosen_animals ) ))

    # Find the second largest predator
    chosen_animals.append(( image_titles[3], find_predator( 1, animal_list, chosen_animals ) ))

    # Find 3 historic animals
    for placement in range( 1, 4 ):

        found_animal = find_large_animal( placement, animal_list, chosen_animals, historic=True )

        if found_animal:

            image_name = "historic_" + str( placement ) 

            image_titles.append( image_name )

            chosen_animals.append(( image_name, found_animal ))

    # Find 6 additional historic herbivores
    for placement in range( 1, 7 ):

        found_animal = find_herbivore( placement, animal_list, chosen_animals, historic=True )

        if found_animal:

            image_name = "herbivore_" + str( placement )

            image_titles.append( image_name )
            chosen_animals.append(( image_name, found_animal ))

    # Find 6 additional historic predators
    for placement in range( 1, 7 ):

        found_animal = find_predator( placement, animal_list, chosen_animals, historic=True )

        if found_animal:

            image_name = "predator_" + str( placement )

            image_titles.append( image_name )
            chosen_animals.append(( image_name, found_animal ))


    write_csvs( "sorted_mammal_info.csv", "chosen_mammals_info.csv", animal_list, chosen_animals )
        
    images_scraper( "chosen_mammals_info.csv" )
        
    # Upload the images to the Google drive 
        
    if upload_bool:
        upload_files( image_titles, "chosen_mammals_info.csv", "slideInfo_BioAdv" )

    
        
        
def find_dobble_images( amount, animal_info, image_titles ):

    dobble_animals = []

    index = 0
    
    round_trip = False
    
    for dobble_image_count in range( 0, amount ):
    
        suitable_animal_found = False
        
        # Print the animal we are on and amount of animals we can choose from 
        print( str( index ) + "/" + str( len( animal_info )) )
        
        # Save the current animal we're looking at
        animal = animal_info[ index ]
            
        # Searching for a suitable animal
        while( not suitable_animal_found ):
               
            if not round_trip:
            
                # Otherwise, check if this animal is historic
                if check_historic( animal ):
                    
                    # If so, move onto the next animal 
                    index += 1
                    animal = animal_info[ index ]
                    
                else:
                    
                    # Check if the animal is already in the dobble list
                    if check_duplicate( animal, dobble_animals ):
                    
                        # If so, move onto the next animal 
                        index += 1
                        animal = animal_info[ index ]
                        
                    else: 
                    
                        # If not, then this is a suitable animal 
                        suitable_animal_found = True
                        
                        
            # Now we have looked through all the animals
            # and we haven't found enough for dobble
            # Now we're allowing duplicates and historic animals 
            else:
                
                # If we have gone thorugh all the animals and haven't found a suitable list of dobble animals, then we will accept duplicates and historic animals
                suitable_animal_found = True
                
            # Check if we have gone around all of the animals we can choose
            if index == ( len( animal_info ) - 1 ):
                    
                # If so, restart our search
                index = 0
   
                # Allow duplicates and historic animals 
                round_trip = True      


        # Add the animal to our dobble list 
        dobble_animals.append( ( "Dobble_" + str( (dobble_image_count ) ), animal_info[ index ] ) )

        # Save the title of the animal
        image_titles.append( "Dobble_" + str( (dobble_image_count ) ) )

        # Move onto the next animal 
        index += 1

        
        
    return dobble_animals


def check_historic( animal ):

    return animal[0] == 'historic'
        
        
def write_csvs( sort_csv, chosen_csv, animal_list, chosen_animals ):

     with open( basest_dir + "/" + sort_csv, mode='w', encoding='utf8' ) as csv_file: 
     
        #os.chmod( basest_dir + "/" + sort_csv, 0o777)
        writer = csv.writer( csv_file )
        
        for animal in animal_list:
            writer.writerow( animal )
            
     logger.log( "done sorting csv" )
     
     with open( basest_dir + "/" + chosen_csv, mode='w', encoding='utf8' ) as csv_file:
     
        #os.chmod( basest_dir + "/" + chosen_csv, 0o777)
        writer = csv.writer( csv_file )
        
        for chosen_animal in chosen_animals:
            row = list( chosen_animal )
            row.extend( list( row[1] ) )
            row.pop(1)
            
            writer.writerow( row )
            
     logger.log( "done writing chosen mammals csv" )
    

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
    
    
    


'''
find template( amount_to_find, animal_list, exemplary_animals, historic, diet ):
    
    Create a list of creatures to be found
    
    Create a blank list of duplicates
    
    Create a variable to keep count of new animals added 
    
    Create the list of creatures 
        
        Define the chosen animal template
        
        Check if it's historic
        
            Check if it's the type of animal we want (diet)
            
                Check if the animal is a duplicate
                
                    Add it to the duplicate list
                
                otherwise
                
                    Add it to the list we're going to return 
        
        Otherwise, it's current
        
            Check if it's the type of animal we want (diet)
            
                Check if the animal is a duplicate
                
                    Add it to the duplicate list 
                
                Othwise
                
                    Add it to the list we're going to return 
        
    Purge duplicates if we need to 
    
    Return them to be extended upon
'''
    
    
    
    
    

def find_predator( placement, animal_list, exemplary_animals, historic=False ):

    placement_counter = placement
    
    # Loop through the list
    for animal in animal_list:
    
        if historic:
        
            if animal[0] == "historic":# and not check_duplicate( animal, exemplary_animals ):
            
                if animal[ DIET ] == "carnivore":
            
                    placement_counter -= 1
                
                    if placement_counter == 0:
                
                        return animal
                        
        else:

            if animal[ 0 ] != "historic": 

                # Check if the animal is a predator
                if animal[ DIET ] == "carnivore" and not check_duplicate( animal, exemplary_animals ):

                    # Subtrack from our placement counter
                    placement_counter -= 1

                    # Check if our placement counter is zero
                    if placement_counter == 0:
                    
                        # If so, return this animal
                        return animal 
    
def find_herbivore( placement, animal_list, exemplary_animals, historic=False ): 
    
    placement_counter = placement
    
    for animal in animal_list:
    
        if historic:
        
            if animal[0] == "historic": #and not check_duplicate( animal, exemplary_animals ):
            
                if animal[ DIET ] == "herbivore":
            
                    placement_counter -= 1
                
                    if placement_counter == 0:
                
                        return animal
                        
        else:
    
            if animal[ 0 ] != "historic" and not check_duplicate( animal, exemplary_animals ):
            
                if animal[ DIET ] == "herbivore":
                
                    placement_counter -= 1
                    
                    if placement_counter == 0:
                    
                        return animal
    
def find_non_predator( placement, animal_list, exemplary_animals, historic=False ):

    placement_counter = placement
    
    for animal in animal_list:
    
        if historic:
        
            if animal[ 0 ] != "historic": # and not check_duplicate( animal, exemplary_animals ):
        
                if animal[ DIET ] == "herbivore" or animal[ DIET ] == "omnivore":
                
                    placement_counter -= 1
                    
                    if placement_counter == 0:
                    
                        return animal
                        
        else:
            
            if animal[ 0 ] != "historic" and not check_duplicate( animal, exemplary_animals ):
        
                if animal[ DIET ] == "herbivore" or animal[ DIET ] == "omnivore":
                
                    placement_counter -= 1
                    
                    if placement_counter == 0:
                    
                        return animal

    

def find_large_animal( placement, animal_list, exemplary_animals, historic=False ):

    placement_counter = placement
    found_animal = False

    for animal in animal_list:

        if placement_counter != 0:

            # Check if  we're searching or historic animals
            if historic:
                
                # Check if the animal is historic
                if animal[ 0 ] == "historic": # and not check_duplicate( animal, exemplary_animals ):

                    placement_counter -= 1
                    
                    if placement_counter == 0:
                        # Save it to our last animal
                        found_animal = animal

            # Otherwise, assume that we're are searching for current animals
            else:

                # Check if the animal is historic
                if animal[ 0 ] != "historic" and not check_duplicate( animal, exemplary_animals ):

                    placement_counter -= 1
                    
                    if placement_counter == 0:
                    
                        # Save it to our last animal
                        found_animal = animal
                    
        

    return found_animal
    
    
def find_smallest_animal( placement, animal_list, exemplary_animals, historic=False ):
    
    found_animal = False
    placement_counter = placement
    
    for index in range( 1, len( animal_list ) + 1):
    
        reverse_index = -1 * index
        
        if historic:
        
            if animal_list[reverse_index][ 0 ] == 'historic':
            
                placement_counter -= 1
                
                if placement_counter == 0:
                
                    found_animal = animal_list[reverse_index] 
                    
        else:
            if animal_list[reverse_index][0] != 'historic' and not check_duplicate( animal_list[reverse_index], exemplary_animals ):
                
                placement_counter -= 1
                
                if placement_counter == 0:
                
                    found_animal = animal_list[reverse_index]
    return found_animal        
     

def upload_files( images, csv_name, target_drive_dir='slideInfo_BioBasic' ):

    logger.log( 'begin file upload' )
    
    client_secrets_path = basest_dir + "/client_secrets.json" 
    credentials_path = basest_dir + "/credentials.txt"
    
    GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = client_secrets_path
        
    # Create google account authentication objects
    gauth = GoogleAuth()

    logger.log( 'Looking for credentials' )
    
    if os.path.exists( credentials_path ):
        logger.log( 'found a credentials' )
        gauth.LoadCredentialsFile( credentials_path )
        

    if gauth.credentials is None:
        logger.log( 'local connect to website' )
        gauth.LocalWebserverAuth()

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

    # Upload the template files to the user
    if target_drive_dir == 'slideInfo_BioBasic':
        upload_template = drive.CreateFile({ 'title': 'TEMPLATE_bio_bas' })
        upload_template.SetContentFile( basest_dir + '/TEMPLATE_bio_bas.pptx' )
        upload_template.Upload()
    
    elif target_drive_dir == 'slideInfo_BioAdv': 
        upload_template = drive.CreateFile({'title': 'TEMPLATE_bio_adv' })
        upload_template.SetContentFile( basest_dir + '/TEMPLATE_bio_adv.pptx' )
        upload_template.Upload()

    ''' Find the name of the folder we want to upload to '''
    # Define the folder we want to upload to 
    target_folder_name = target_drive_dir
    target_folder_id = ''

    # Find the list of all of the files in the google drive 
    file_list = drive.ListFile({ 'q': "'root' in parents and trashed=false"}).GetList()

    # Loop through all of the files in the 
    for file_object in file_list:

        # Check if the current one is our target
        if file_object[ 'title' ] == target_folder_name:

            # Save the folder id
            target_folder_id = file_object[ 'id' ]        

    logger.log( "folder id: " + target_folder_id )
    
    # upload the CSV containing only the info on the chosen animals for images
    upload_csv = drive.CreateFile({'title': csv_name, 'parents': [{'id': target_folder_id }] })
    upload_csv.SetContentFile( basest_dir + "/" + csv_name )
    upload_csv.Upload()
    logger.log( "uploaded chosen_mammals csv" )
    
    # Loop through the images
    for image_name in images: 
        upload_image = drive.CreateFile( {'title': image_name, 'parents': [{'id': target_folder_id }]})
        
        #upload_image.SetContentFile( "python_scripts/biodiversity/animal_images/" + image_name )

        logger.log( image_name )
        
        if __name__ == "__main__":
            upload_image.SetContentFile( "animal_images/" + image_name + ".jpg")
            
        else:
            upload_image.SetContentFile( basest_dir + '/animal_images/'+ image_name + ".jpg")
        
        upload_image.Upload()
	

def check_duplicate( animal, animal_info ):

    # Loop through the animal array 
    for potential_duplicate in animal_info:
    
        #logger.log( potential_duplicate )
        # Check if the binomial is the same as in the array 
        if animal[ BINOMIAL ] == potential_duplicate[1][BINOMIAL]:
        
            return True
    # If no duplicate was found, return false 
    return False

if __name__ == "__main__":
	main()
	
