import time
import requests
try:
    from python_scripts.biodiversity.enviro_log import enviro_logger

except:
    from biodiversity.enviro_log import enviro_logger


logger = enviro_logger()
logger.restart()

result = requests.get( "https://www.google.com/" )
logger.log( result.status_code )

logger.log( "went all the way through" )
