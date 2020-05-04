from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver
import time

cmd_options = FirefoxOptions()
cmd_options.headless = True


print( "sleeping 10 seconds" )
time.sleep( 10 )

attempts = 3
while( attempts > 0 ):
	try:
		driver = webdriver.Firefox(options=cmd_options, executable_path = '/usr/bin/geckodriver' )
		driver.get("https://www.google.com/")
		print (driver.title)

		driver.close()
		attempts = 0
	except: 
		print( "failed again" )
		attempts -= 1

print( "went all the way through" )
