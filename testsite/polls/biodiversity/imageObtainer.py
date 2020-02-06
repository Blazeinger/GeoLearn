from PIL import Image
import requests
from io import BytesIO
from StringIO import StringIO

response = requests.get( "https://en.wikipedia.org/wiki/Montane_vole" )
picture = StringIO( response.content )
img = Image.open( picture )
