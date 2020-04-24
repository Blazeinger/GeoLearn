import csv
import os
import random
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

if __name__ == "__main__":
    from biodiversity_image_scraper import images_scraper
else:
    from .biodiversity_image_scraper import images_scraper


MASS = 16
BINOMIAL = 1
ANIMAL_TITLE = 0
ANIMAL_OBJECT = 1
ENDANGERED_STATUS = 5
ORDER = 9
DIET = 22
NON_PREDATOR_ORDERS = [ "PROTURA", "EMBIOPTERA", "ZORAPTERA", "ISOPTERA", "MALLOPHAGA", "ANOPLURA", "HOMOPTERA", "SIPHONAPTERA" ] 

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    find_animal_images( 'mammal_info.csv', True, "animal_images" )

def find_animal_images( csv_name, upload_bool, dir_name ):
    # Open CSV file
    with open( csv_name ) as csv_file:

        animal_reader = csv.reader( csv_file, delimiter=',' )

        # Create a list with the animals from the csv
        animal_list = create_list_from_csv( animal_reader )

        # Sort the list of animals
        sort_results( animal_list )

        print( "animal list sorted" ) 

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
        exemplary_animals.append(( image_titles[2], animal_list[ len( animal_list)-1 ] ))

        # Find the second smallest animal
        exemplary_animals.append(( image_titles[3], animal_list[ len( animal_list ) - 2 ] ))
        

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
        for placement in range( 3, 8 ):
        
            found_animal = find_large_animal( placement, animal_list, exemplary_animals, True )
            
            if found_animal:
            
                exemplary_animals.append(( "historic_" + str( placement - 2 ), found_animal ))
                
                image_titles.append( "historic_" + str( placement - 2 ) )
            
        

        dobble_count = 28
        dobble_offset = 0
        index = 0
        dobble_animals = []

        for dobble_image_count in range( 0, dobble_count ):
        
            animal = animal_list[ index ]
            
            duplicate_check = True
            
            while( duplicate_check ):
            
                if check_duplicate( animal, dobble_animals ):
                    
                    index += 1
                    
                    animal = animal_list[ index ]
                    
                else:
                    
                    duplicate_check = False
            
            dobble_number = dobble_image_count - dobble_offset

            dobble_animals.append( ( "Dobble_" + str( (dobble_image_count ) ), animal_list[ index ] ) )

            image_titles.append( "Dobble_" + str( (dobble_image_count ) ) )

            index += 1

            if index == len( animal_list ):
                    
                index = 0

        exemplary_animals.extend( dobble_animals )
            
        # Initialize a list for the names of the images 
        image_names = []

        print( "saved animal info" )
        
        with open( "sorted_mammal_info.csv", mode='w' ) as csv_file:
        	writer = csv.writer( csv_file )
        	
        	for animal in animal_list:
        		writer.writerow( animal )
        	
        print( "done sorting csv" )
        
        with open( "chosen_mammals_info.csv", mode='w' ) as csv_file:
        
                writer = csv.writer( csv_file )
                
                for chosen_animal in exemplary_animals:
                
                        row = list(chosen_animal )
                        
                        row.extend( list( row[1] ) )
                        row.pop(1)
                        
                        writer.writerow( row )
                        
        print( "done writing chosen mammals csv" )
        
        #for animal in exemplary_animals:
        #    print( animal[1][1] )
        
        # Download the images for all of the animals we want 

        #for animal in exemplary_animals:
        
        #	image_names.append( animal[1][1] )
        #
        images_scraper( dir_name, exemplary_animals, image_titles )
        
        # Upload the images to the Google drive 
        
        if upload_bool:
            upload_files( image_titles, "chosen_mammals_info.csv" )
        
                            
    

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

def find_predator( placement, animal_list, exemplary_animals, historic=False ):

    placement_counter = placement
    
    # Loop through the list
    for animal in animal_list:
    
        if historic:
        
            if animal[0] == "historic" or animal[5] == "Extinct":# and not check_duplicate( animal, exemplary_animals ):
            
                if animal[ DIET ] == "carnivore":
            
                    placement_counter -= 1
                
                    if placement_counter == 0:
                
                        return animal
                        
        else:

            if animal[ 0 ] != "historic" and animal[5] != "Extinct": 

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
        
            if animal[0] == "historic" or animal[5] == "Extinct": #and not check_duplicate( animal, exemplary_animals ):
            
                if animal[ DIET ] == "herbivore":
            
                    placement_counter -= 1
                
                    if placement_counter == 0:
                
                        return animal
                        
        else:
    
            if animal[ 0 ] != "historic" and animal[5] != "Extinct" and not check_duplicate( animal, exemplary_animals ):
            
                if animal[ DIET ] == "herbivore":
                
                    placement_counter -= 1
                    
                    if placement_counter == 0:
                    
                        return animal
    
def find_non_predator( placement, animal_list, exemplary_animals, historic=False ):

    placement_counter = placement
    
    for animal in animal_list:
    
        if historic:
        
            if animal[ 0 ] != "historic" and animal[5] != "Extinct": # and not check_duplicate( animal, exemplary_animals ):
        
                if animal[ DIET ] == "herbivore" or animal[ DIET ] == "omnivore":
                
                    placement_counter -= 1
                    
                    if placement_counter == 0:
                    
                        return animal
                        
        else:
            
            if animal[ 0 ] != "historic" and animal[5] != "Extinct" and not check_duplicate( animal, exemplary_animals ):
        
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
                if animal[ 0 ] == "historic" or animal[5] == "Extinct": # and not check_duplicate( animal, exemplary_animals ):

                    placement_counter -= 1
                    
                    if placement_counter == 0:
                        # Save it to our last animal
                        found_animal = animal

            # Otherwise, assume that we're are searching for current animals
            else:

                # Check if the animal is historic
                if animal[ 0 ] != "historic" and animal[5] != "Extinct" and not check_duplicate( animal, exemplary_animals ):

                    placement_counter -= 1
                    
                    if placement_counter == 0:
                    
                        # Save it to our last animal
                        found_animal = animal
                    
        

    return found_animal
            

def upload_files( images, csv_name ):

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
    target_folder_name = 'slideInfo_Bio'
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
    
    # upload the CSV containing only the info on the chosen animals for images
    upload_csv = drive.CreateFile({'title': csv_name, 'parents': [{'id': target_folder_id }] })
    upload_csv.SetContentFile( csv_name )
    upload_csv.Upload()
    print( "uploaded chosen_mammals csv" )
    
    # Loop through the images
    for image_name in images: 
        upload_image = drive.CreateFile( {'title': image_name, 'parents': [{'id': target_folder_id }]})
        
        #upload_image.SetContentFile( "python_scripts/biodiversity/animal_images/" + image_name )

        print( image_name )
        
        if __name__ == "__main__":
            upload_image.SetContentFile( "animal_images/" + image_name + ".jpg")
            
        else:
            print( BASE_DIR)
            upload_image.SetContentFile( "python_scripts/biodiversity/animal_images/" + image_name + ".jpg")
        
        upload_image.Upload()

def check_duplicate( animal, animal_info ):

    # Loop through the animal array 
    for potential_duplicate in animal_info:
    
        #print( potential_duplicate )
        # Check if the binomial is the same as in the array 
        if animal[ BINOMIAL ] == potential_duplicate[1][BINOMIAL]:
        
            return True
    # If no duplicate was found, return false 
    return False

if __name__ == "__main__":
	main()
	
