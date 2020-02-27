import csv
import os
from biodiversity_image_scraper import image_scraper

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

	# Find the second largest animal
        image_scraper( find_smallest_animal( animal_reader ) )

	# Find the smallest animal

    
def find_largest_animal( animal_reader ):

    ANIMAL_MASS = 17
    ANIMAL_BINOMIAL = 1
    
    index = 0
    biggest_animal_mass = 0
    biggest_animal_binomial = ''
    for row in animal_reader:

        # Skip the 0 index, since it's just the column names
        
        # Check if the index is 1
        if index == 1:
            biggest_animal_binomial = row[ ANIMAL_BINOMIAL ]
            biggest_animal_mass = row[ ANIMAL_MASS ]

        # Check if the current animal is bigger than the biggest sofar
        elif index != 0:
            if row[ ANIMAL_MASS ] > biggest_animal_mass:
                biggest_animal_binomial = row[ ANIMAL_BINOMIAL ]
                biggest_animal_mass = row[ ANIMAL_MASS ]

        # Increment our index 
        index += 1

    # Now that we know the biggest animal, return the scientific name of the animal
    return biggest_animal_binomial

def find_smallest_animal( animal_dict ):

    ANIMAL_MASS = 17
    ANIMAL_BINOMIAL = 1
    
    index = 0
    smallest_animal_mass = 0
    smallest_animal_binomial = ''
    for row in animal_reader:

        # Skip the 0 index, since it's just the column names
        
        # Check if the index is 1
        if index == 1:
            smallest_animal_binomial = row[ ANIMAL_BINOMIAL ]
            smallest_animal_mass = row[ ANIMAL_MASS ]

        # Check if the current animal is bigger than the biggest sofar
        elif index != 0:
            if row[ ANIMAL_MASS ] < smallest_animal_mass:
                smallest_animal_binomial = row[ ANIMAL_BINOMIAL ]
                smallest_animal_mass = row[ ANIMAL_MASS ]

        # Increment our index 
        index += 1

    # Now that we know the biggest animal, return the scientific name of the animal
    return smallest_animal_binomial

if __name__ == "__main__":
    main()
