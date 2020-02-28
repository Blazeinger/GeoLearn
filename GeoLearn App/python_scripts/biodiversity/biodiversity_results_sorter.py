import csv
import os
from biodiversity_image_scraper import image_scraper

ANIMAL_MASS = 16
ANIMAL_BINOMIAL = 1

def main():
    sort_results( 'mammal_info_35.0_-111.0.csv' )

def sort_results( csv_name ):
    # Open CSV file
    with open( csv_name ) as csv_file:
        animal_reader = csv.reader( csv_file, delimiter=',' )

        # Create our list that contains exemplary animals 
        exemplary_animals = []

        # Find the largest animal
        image_scraper( find_largest_animal( animal_reader ) )

        # Reset the csv file to the top of the document
        csv_file.seek(0)
        print( "done with largest" )

	# Find the second largest animal
        

	# Find the smallest animal
        image_scraper( find_smallest_animal( animal_reader ) )

        print( "done with smallest" )

    
def find_largest_animal( animal_reader ):
    
    index = 0
    for row in animal_reader:

        # Skip the 0 index, since it's just the column names
        
        # Check if the index is 1
        if index == 1:
            biggest_animal_binomial = row[ ANIMAL_BINOMIAL ]
            biggest_animal_mass = float( row[ ANIMAL_MASS ] )

        # Check if the current animal is bigger than the biggest sofar
        elif index != 0:
            if float( row[ ANIMAL_MASS ] ) > biggest_animal_mass:
                
                biggest_animal_binomial = row[ ANIMAL_BINOMIAL ]
                biggest_animal_mass = float( row[ ANIMAL_MASS ] )

        # Increment our index 
        index += 1

    # Now that we know the biggest animal, return the scientific name of the animal
    print( biggest_animal_binomial )
    return biggest_animal_binomial

def find_smallest_animal( animal_reader ):
    
    index = 0
    for row in animal_reader:

        # Skip the 0 index, since it's just the column names
        
        # Check if the index is 1
        if index == 1:
            smallest_animal_binomial = row[ ANIMAL_BINOMIAL ]
            smallest_animal_mass = float( row[ ANIMAL_MASS ] )

        # Check if the current animal is bigger than the biggest sofar
        elif index != 0:
            if float( row[ ANIMAL_MASS ] ) < smallest_animal_mass:
                smallest_animal_binomial = row[ ANIMAL_BINOMIAL ]
                smallest_animal_mass = float( row[ ANIMAL_MASS ] )

        # Increment our index 
        index += 1

    # Now that we know the biggest animal, return the scientific name of the animal
    print( smallest_animal_binomial )
    return smallest_animal_binomial

if __name__ == "__main__":
    main()
