import time
import requests
try:
    from python_scripts.biodiversity.enviro_log import enviro_logger

except:
    from biodiversity.enviro_log import enviro_logger


logger = enviro_logger()
logger.restart()

app_script_url = "https://script.google.com/macros/s/AKfycbwiCl5ILpsHtKbr6sK3fupy575qN2GAr1MsPp6EI4c/dev?userEmail=joshusttenakhongva@gmail.com&schoolName=requestTest"

result = str( requests.get( app_script_url ).content).split( '\\n' )

for line in result:
	print( line )
