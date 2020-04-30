import time
import os
import csv

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

def main():

    test_strings = [ "test 1",
                     "test 2",
                     "test 3",
                     ]

    write_csv_name = BASE_DIR + "/test_write.csv"
    
    print( BASE_DIR )

    with open( write_csv_name, mode='w', encoding='utf8' ) as csv_file:
        os.chmod( write_csv_name, 0o777)
        writer = csv.writer( csv_file )

        for line in test_strings:
            writer.writerow( line )

    with open( write_csv_name, encoding='utf8' ) as csv_file:

        reader = csv.reader( csv_file )
        
        for line in reader:
            print( line )


if __name__ == "__main__":
    main()
