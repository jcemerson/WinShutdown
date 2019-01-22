##### WinShutdown.py v1.5; 01-21-2019 #####
##### Jordan Emerson; WutDuk?         #####
##### https://github.com/jcemerson    #####
###########################################


# Redirect stderr to support use of pythonw.exe in order to run without cmd console
import sys, os
if sys.executable.endswith( "pythonw.exe" ):
  sys.stdout = open( os.devnull, "w" );
  sys.stderr = open( os.path.join( os.getenv( "TEMP" ), "stderr-"+os.path.basename( sys.argv[ 0 ] ) ), "w" )


import KivyConfigCheck
import kivy
from WinShutdown import WinShutdownTimer, ImminentPopup, FinalPopup
from kivy import Config
from kivy.app import App


# Script to update settings for Windows 10 issues -- See KivyConfigCheck.py for details
KivyConfigCheck.WindowsCheck()


# Set config.ini setting for this instance of the app only (as opposed to writing to the file which would impact ALL Kivy apps)
Config.set( 'graphics', 'fullscreen', 0 )
Config.set( 'graphics', 'resizable', 0 )
Config.set( 'kivy', 'exit_on_escape', 0 )
Config.set( 'kivy', 'window_icon', '.\Images\power-on.png')


# Supported Kivy version required for operation. Older version may work too, but they're not supported. You can remove or modify this setting at your own risk.
kivy.require( '1.10.1' )

# App class that, when called, instatiates the root class
class WinShutdownApp( App ):

    def build( self ):
        shutdown_timer = WinShutdownTimer()
        shutdown_timer.systray.start()
        return shutdown_timer


#Instantiate top-level/root widget and run it
if __name__ == "__main__":
    WinShutdownApp().run()
