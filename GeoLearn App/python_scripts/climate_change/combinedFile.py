import mysql.connector
import ffmpy
import time
import csv
import sys
import os
import ee
import sys
import os

from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
from ee import batch

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

latitude_val = float(sys.argv[1])
longitude_val = float(sys.argv[2])

manipulated_lat = latitude_val + 0.2
manipulated_lng = longitude_val + 0.2

ee.Initialize()

# Define the image collection we will be using
collection = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA')

# Creates a polygon which will be used as the bounds of the image
# Flagstaff Long: -111.6512, Lat: 35.1982
# region_polygon = ee.Geometry.Polygon(
#     [[[-111.791491098128,35.150445194872816],
#       [-111.49829346629207,35.150445194872816],
#       [-111.49829346629207,35.385344417919924],
#       [-111.791491098128,35.385344417919924],
#       [-111.791491098128,35.150445194872816]]])

region_polygon = ee.Geometry.Polygon(
[[[longitude_val, latitude_val],
  [manipulated_lng, latitude_val],
  [manipulated_lng, manipulated_lat],
  [longitude_val, manipulated_lat],
  [longitude_val, latitude_val]]]
)


# Define the time range
collection_time = collection.filterDate('2013-04-11', '2019-07-01') # YYYY-MM-DD

# Select location based on location of tile
# path = collection_time.filter(ee.Filter.eq('WRS_PATH', 37))
# pathrow = path.filter(ee.Filter.eq('WRS_ROW', 32))

# Select location based on Geo Location
point_geom = ee.Geometry.Point(longitude_val, latitude_val) # long, lat
pathrow = collection_time.filterBounds(point_geom)

# Select imagery with less than 5% cloud coverage
clouds = pathrow.filter(ee.Filter.lt('CLOUD_COVER', 5))

# Select bands (RGB Respectively)
bands = clouds.select(['B4', 'B3', 'B2'])

# Make the data 8 bit
def convertBit(image):
  return image.multiply(512).uint8()

# Convert bands to output video
outputVideo = bands.map(convertBit)
print("Beginning video creation...\n")

# Export video to Google Drive
out = batch.Export.video.toDrive(outputVideo, description='Region_Timelapse',
	                         dimensions=720, framesPerSecond = 2,
	                         region = region_polygon, maxFrames = 10000)

# Process the image
process = batch.Task.start(out)
print("Video sent to drive...\n")

#run download, conversion, and upload

# Create google account authentication objects
gauth = GoogleAuth('settings.yaml')
drive = GoogleDrive(gauth)

if os.path.exists( 'credentials.txt' ):
   gauth.LoadCredentialsFile( 'credentials.txt' )

if gauth.credentials is None:
   gauth.LocalWebserverAuth()

elif gauth.access_token_expired:
   gauth.Refresh()

else:
   gauth.Authorize()

#need to wait until file is created in Drive
restart = True
while restart:
    #refresh file list of Drive files
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()

    #iterate through file list
    for file1 in file_list:

        if file1['title'] == 'Region_Timelapse.mp4':

            print('Downloading file %s from Google Drive' % file1['title'])
            file1.GetContentFile('toConvert.mp4')
            restart = False
            break

        else:
            #print("Waiting for video in Drive\n")
            time.sleep(10)

#define params for conversion
ff = ffmpy.FFmpeg(inputs = {'toConvert.mp4': None},
  outputs = {'convertedVid.gif': None})

#begin video conversion
print("Converting mp4 to GIF")
ff.run()

target_folder_name = 'slideInfo_Climate'
target_folder_id = ''

file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()

#loop through all files in drive
for i in file_list:

    #if current one is the target folder
    if i['title'] == target_folder_name:

        #save the folder id
        target_folder_id = i['id']

#create a new file in the Drive and give it the converted
#gif as its "content". Upload that schtuff.
newDriveFile = drive.CreateFile({'title': 'time_lapse.gif', 'parents': [{'id': target_folder_id}]})
newDriveFile.SetContentFile('convertedVid.gif')
newDriveFile.Upload()
print("Uploaded GIF to Drive as %s" % newDriveFile['title'])

#delete local files to save storage
os.remove("toConvert.mp4")
os.remove("convertedVid.gif")
print("Files removed from local machine")
