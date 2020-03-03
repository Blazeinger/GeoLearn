import mysql.connector
import csv
import sys
import os

# pip3 install pydrive
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

def main():
	google_oauth()

def google_oauth():

	# Create google account authentication objects
	gauth = GoogleAuth('settings.yaml')
	
	if os.path.exists( 'credentials.txt' ):
		gauth.LoadCredentialsFile( 'credentials.txt' )
	
	if gauth.credentials is None:
		print( 'local webserver branch' )
		gauth.LocalWebserverAuth()
		
	elif gauth.access_token_expired:
		print( 'refresh branch' )
		gauth.Refresh()
		
	else:
		print( 'authorize branch' )
		gauth.Authorize()
	
	print( 'client secrets 2' )
		
	gauth.SaveCredentialsFile( 'credentials.txt' )

if __name__ == "__main__":
	main()
