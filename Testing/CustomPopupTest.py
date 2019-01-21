import kivy
from kivy import Config
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.properties import StringProperty, NumericProperty
from kivy.animation import Animation

kivy.require( '1.10.1' )

Config.set( 'graphics', 'fullscreen', 0 )
Config.set( 'graphics', 'height', 600 )
Config.set( 'graphics', 'width', 800 )
Config.set( 'graphics', 'resizable', 0 )
Config.set( 'kivy', 'exit_on_escape', 1 )
# # Define Window attributes
from kivy.core.window import Window

Window.size = ( 800, 600 )
Window.fullscreen = False



class CustomPopup( Popup ):

    countdown = NumericProperty( 0 )
    # text_1 = StringProperty( '' )


    def __init__( self, foo = 'bar' ):
        super( CustomPopup, self ).__init__()
        self.foo =  foo
        # self.text_1 =  'blah blah {foo}'.format( foo = self.foo )
        self.title = 'Title {foo}!'.format( foo = self.foo )
        print(self.countdown)


    def start_stop_timer( self ):
        Animation.cancel_all( self )
        if self.countdown > 0:
            print(self.countdown)
            self.anim = Animation( countdown = 0, duration = self.countdown )
            self.anim.start( self )
            self.anim.bind( on_complete = self.narg )
        else:
            print(self.countdown)
            self.countdown = ( 5 * 2 )
            print(self.countdown)
            self.anim = Animation( countdown = 0, duration = self.countdown )
            self.anim.start( self )
            self.anim.bind( on_complete = App.get_running_app().stop )

    def narg( self, *args ):
        print('blaaaaaaaaaaaaaaaaaarg!')

class CustomPopupTestApp( App ):
    def build( self ):
        blarg = CustomPopup()
        return blarg



#Instantiate top-level/root widget and run it
if __name__ == "__main__":
    CustomPopupTestApp().run()
