import csv
import os
from biodiversity_image_scraper import image_scraper

MASS = 16
BINOMIAL = 1

def main():
    find_animal_images( 'mammal_info_35.0_-111.0.csv' )

def find_animal_images( csv_name ):
    # Open CSV file
    with open( csv_name ) as csv_file:
        animal_reader = csv.reader( csv_file, delimiter=',' )

        # Create a list with the animals from the csv
        animal_list = create_list_from_csv( animal_reader )

        # Sort the list of animals
        sort_results( animal_list )

        # Create our list that contains exemplary animals 
        exemplary_animals = []

        # Find the largest animal
        exemplary_animals.append( ("largest_animal", animal_list[ 0 ]) )
        
        # Find the second largest animal 
        exemplary_animals.append( ("second_largest_animal", animal_list[ 1 ] ) )

        # Find the smallest animal
        exemplary_animals.append( ("smallest_animal", animal_list[ len( animal_list)-1 ] ) )

        # Find the second smallest animal
        exemplary_animals.append( ("second_smallest_animal", animal_list[ len( animal_list ) - 2 ] ) )

        for animal in exemplary_animals:

            image_scraper( animal[1][ BINOMIAL ], "animal_images", animal[0] )

                            
    

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


def find_predatory_animal( placement ):
    return True
    

if __name__ == "__main__":
    main()
