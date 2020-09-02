from google_images_download import google_images_download
import os
import getpass
response = google_images_download.googleimagesdownload()

CURR_DIR = os.path.dirname( os.path.realpath(__file__) )
ANIMAL_DIR = CURR_DIR + '/animal_images' 

print( CURR_DIR )
print( ANIMAL_DIR )

search_query = 'Sonic the Hedgehog'

arguments = {"keywords": search_query, 
             "limit":1, 
             "print_urls":True, 
             "format":"jpg", 
             "output_directory": CURR_DIR, 
             "image_directory": "animal_images" }

#print( 'user: ' + getpass.getuser() )

#os.system( 'sudo mkdir downloads/' + ('\ '.join( search_query.split()) + '2' ))

paths = response.download(arguments)

def correct_query( query ):

    return '\ '.join( query.split() )
