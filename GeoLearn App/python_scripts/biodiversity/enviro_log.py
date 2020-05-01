import os 

class enviro_logger():
    
    def __init__( self ):
        
        self.path = os.path.dirname( os.path.realpath(__file__)).replace( "/python_scripts/biodiversity", "" )
        self.text_file_path = self.path + "/log_output.txt" 
        
        
    def log( self, string ):
        print( str( string ) )
        with open( self.text_file_path, mode='a', encoding='utf8' ) as txt_file:
            txt_file.write( str( string ) + "\n" )
            
    def restart( self ):
	
        with open( self.text_file_path, mode='w', encoding='utf8' ) as txt_file:
            txt_file.write( "" )
            print( "output log cleared" )
