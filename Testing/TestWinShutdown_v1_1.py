# import KivyConfigCheck
import subprocess
import pystray
import kivy
from kivy import Config
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.popup import Popup
# from kivy.uix.slider import Slider
from kivy.animation import Animation
from kivy.properties import StringProperty, NumericProperty, BooleanProperty, ListProperty


kivy.require( '1.10.1' )

# # Script to update settings for Windows 10 issues
# KivyConfigCheck.WindowsCheck()

# Set fixed window size and non-resizable
Config.set( 'graphics', 'fullscreen', 0 )
Config.set( 'graphics', 'height', 600 )
Config.set( 'graphics', 'width', 800 )
Config.set( 'graphics', 'resizable', 0 )
Config.set( 'kivy', 'exit_on_escape', 0 )
Config.set( 'kivy', 'window_icon', '.\Images\power-on.png')
Config.set( 'graphics', 'multisamples', 0 )


# import Window for Keybindings functionality
from kivy.core.window import Window

# Define Window attributes
Window.size = ( 800, 600 )
Window.fullscreen = False

# s = Slider( value_track = True, value_track_color = [ 1, 0, 0, 1 ] )



class ImminentPopup( Popup ):

    label_text = StringProperty( '' )

    def __init__( self, cmd ):
        super( ImminentPopup, self ).__init__()
        self.title = 'Imminent {cmd}!'.format( cmd = cmd )
        self.label_text = 'By forcing an active countdown to 00:00:00 you are about to initiate an [i][b]imminent {cmd}[/b][/i].\n\nDo you wish to continue?'.format( cmd = cmd )



class FinalPopup( Popup ):

    countdown = NumericProperty( 5.9 )

    def __init__( self, cmd ):
        super( FinalPopup, self ).__init__()
        print('FinalPopup instantiated')


    def start_final_timer( self ):
        print('final timer started')
        Animation.cancel_all( self )
        self.anim = Animation( countdown = 0, duration = self.countdown )
        self.anim.bind( on_complete = App.get_running_app().stop )
        self.anim.start( self )



class TestWinShutdownTimer( GridLayout, ToggleButtonBehavior ):
    print( 'TestWinShutdownTimer initialized')
    # Define default attributes
    font_size = 20
    widget_padding = ( 25, 10, 25, 10 )
    spacer_width = 10
    start_pause = StringProperty( 'Start' )
    start_pause_disabled = BooleanProperty( True )
    sub_time_disabled = BooleanProperty( True )
    add_time_disabled = BooleanProperty( False )
    preset_disabled = BooleanProperty( False )
    abort_disabled = BooleanProperty( True )
    countdown = NumericProperty( 0 )
    abort_background_color = ListProperty( [ 1, 1, 1, 1 ] )


    def __init__( self ):
        super( TestWinShutdownTimer, self ).__init__()
    # Set Keybinding to the Window
        Window.bind( on_key_down = self.key_action )
        if self.ids.shutdown.state == 'down':
            cmd = 'Shutdown'
        elif self.ids.restart.state == 'down':
            cmd = 'Restart'
        elif self.ids.hibernate.state == 'down':
            cmd = 'Hibernate'
        else:
            cmd = 'Log Off'

        self.im_popup = ImminentPopup( cmd )
        self.final_popup = FinalPopup( cmd )

    # Define keybinding logic
    # I'm not exactly sure what "arg" is capturing, I just know I needed to capture the argument for this to work
    def key_action( self, keyboard, keycode, arg, text, modifiers ):
        print( keycode, text, modifiers, arg )
        if self.preset_disabled == False:

            # cmd buttons
            if keycode == 115 and text == 's' and modifiers == []:
                self.ids.shutdown.trigger_action( 0 )
            elif keycode == 114 and text == 'r' and modifiers == []:
                    self.ids.restart.trigger_action( 0 )
            elif keycode == 104 and text == 'h' and modifiers == []:
                    self.ids.hibernate.trigger_action( 0 )
            elif keycode == 108 and text == 'l' and modifiers == []:
                    self.ids.logoff.trigger_action( 0 )

            # preset duration buttons
            elif keycode == 50 and text == '2' and modifiers == []:
                    self.ids.set20.trigger_action( 0 )
            elif keycode == 52 and text == '4' and modifiers == []:
                    self.ids.set40.trigger_action( 0 )
            elif keycode == 54 and text == '6' and modifiers == []:
                    self.ids.set60.trigger_action( 0 )
            elif keycode == 57 and text == '9' and modifiers == []:
                    self.ids.set90.trigger_action( 0 )
            elif keycode == 59 and text == '1' and modifiers == []:
                    self.ids.set120.trigger_action( 0 )

        # subtract time / add time buttons
        if self.sub_time_disabled == False:
            if ( keycode == 276 and text == None and modifiers == [] ) or ( keycode == 45 and text == '-' and modifiers == [] ) or ( keycode == 269 and text == 'č' and modifiers == [] ):
                self.ids.minus15.trigger_action( 0 )

        if self.add_time_disabled == False:
            if ( keycode == 275 and text == None and modifiers == [] ) or ( keycode == 61 and text == '=' and modifiers == [ 'shift' ] ) or ( keycode == 270 and text == 'Ď' and modifiers == [] ):
                self.ids.plus15.trigger_action( 0 )

        # Start/Stop buttons
        if self.countdown > 0 and self.start_pause_disabled == False:
            if keycode == 32 and text == ' ' and modifiers == []:
                self.ids.start_pause.trigger_action( 0 )

        # Abort button
        if  self.abort_disabled == False:
            if keycode == 97 and text == 'a' and modifiers == []:
                self.ids.abort.trigger_action( 0 )

        # Popup Yes/No buttons
        if keycode == 121 and text == 'y' and modifiers == []:
            self.im_popup.ids.yes.trigger_action( 0 )
        elif keycode == 110 and text == 'n' and modifiers == []:
            self.im_popup.ids.no.trigger_action( 0 )


    def initiate_shutdown( self, *args ):
        print( 'initiate_shutdown() called' )
        # Provide the reason for the restart or shutdown. These events are documented as "Other Planned"
        d_cmd = '/d p:0:0'
        # Comment on the reason for the restart or shutdown.
        c_cmd = '/c "Automated User-initiated {cmd} via WinShutdown.py"'
        # build final cmd
        final_cmd = ''
        if self.start_pause == 'Pause' and self.countdown == 0:
            if self.ids.shutdown.state == 'down':
                final_cmd = 'shutdown /s' + ' ' + d_cmd + ' ' + c_cmd.format( cmd = 'Shutdown')
            elif self.ids.restart.state == 'down':
                final_cmd = 'shutdown /r' + ' ' + d_cmd + ' ' + c_cmd.format( cmd = 'Restart')
            elif self.ids.hibernate.state == 'down':
                final_cmd = 'shutdown /h'
            else:
                final_cmd = 'shutdown /l'
            # send final cmd to windows cmd shell
            # subprocess.call( final_cmd, shell = True )
            print( final_cmd )
            # App.stop()
            self.final_popup.open()


    def set_timer( self, button_time ):
        print( 'set_timer() called' )
        if self.countdown == 0:
            self.countdown = button_time


    def clear_timer( self ):
        print( 'clear_timer() called; ' + str( self.countdown ) )
        self.countdown = 0


    def toggle_sub_time_status( self ):
        print( 'toggle_sub_time_status() called; ' + self.ids.start_pause.state + '; ' + str( self.countdown ) + '; ' + str( self.sub_time_disabled ) + '; ' + str( self.ids.minus15.disabled ) )
        if self.countdown < 15 * 60:
            self.sub_time_disabled = True
        else:
            self.sub_time_disabled = False


    def toggle_add_time_status( self ):
        print( 'toggle_add_time_status() called; ' + self.ids.start_pause.state + '; ' + str( self.countdown ) + '; ' + str( self.add_time_disabled ) )
        if self.add_time_disabled == False:
            self.add_time_disabled = True
        elif self.countdown == 0 or self.add_time_disabled == True:
            self.add_time_disabled = False


    def toggle_start_pause_status( self ):
        print( 'toggle_start_pause_status() called; ' + str( self.countdown ) + '; ' + str( self.start_pause_disabled ) )
        if self.countdown > 0:
            self.start_pause_disabled = False
        else:
            self.start_pause_disabled = True


    def toggle_abort_status( self ):
        print( 'toggle_abort_status() called; ' + str( self.countdown ) + '; ' + self.ids.start_pause.state + '; ' + str( self.abort_disabled ) )
        if self.countdown > 0 and self.ids.start_pause.state == 'down':
            self.abort_disabled = False
            self.abort_background_color = [ 1, 0, 0, 1 ]
        else:
            self.abort_disabled = True
            self.abort_background_color = [ 1, 1, 1, 1 ]


    def toggle_preset_status( self ):
        print( 'toggle_preset_status() called; ' + self.ids.start_pause.state + '; ' + str( self.preset_disabled ) )
        if self.ids.start_pause.state == 'down':
            self.preset_disabled = True
        else:
            self.preset_disabled = False


    def toggle_start_pause_state( self ):
        print( 'toggle_start_pause_state() called; ' + self.start_pause + '; ' + self.ids.start_pause.state )
        if self.start_pause == 'Start':
            self.ids.start_pause.state = 'normal'
        else:
            self.ids.start_pause.state = 'down'


    def toggle_preset_state( self ):
        print( 'toggle_preset_state() called; ' + str( self.countdown ) + '; ' + self.ids.set20.state + '; ' + self.ids.set40.state + '; ' + self.ids.set60.state + '; ' + self.ids.set90.state + '; ' + self.ids.set120.state )
        # Perhaps build a dict instead of list using button id as key and state as value?
        if self.countdown == 0:
            self.ids.set20.state = 'normal'
            self.ids.set40.state = 'normal'
            self.ids.set60.state = 'normal'
            self.ids.set90.state = 'normal'
            self.ids.set120.state = 'normal'


    def toggle_cmd_state( self ):
        print( 'toggle_cmd_state() called; ' + str( self.ids.shutdown.state ) + '; ' + str( self.ids.restart.state ) + '; ' + str( self.ids.hibernate.state ) + '; ' + str( self.ids.logoff.state ) )
        self.ids.shutdown.state = 'normal'
        self.ids.restart.state = 'normal'
        self.ids.hibernate.state = 'normal'
        self.ids.logoff.state = 'normal'


    def toggle_start_pause_text( self ):
        print( 'toggle_start_pause_text() called; ' + self.ids.start_pause.state + '; ' + str( self.countdown ) + '; ' + self.start_pause )
        if self.ids.start_pause.state == 'down' and self.countdown > 0:
            self.start_pause = 'Pause'
        else:
            self.start_pause = 'Start'


    def start_stop_timer( self ):
        print( 'start_stop_timer() called; ' + self.ids.start_pause.state + '; ' + str( self.countdown ) )
        # Cancel any current animation in progress
        Animation.cancel_all( self )
        # Define the rules for Animation; i.e., ( <where we are going>, <where we're coming from> )
        self.anim = Animation( countdown = 0, duration = self.countdown )
        if self.ids.start_pause.state == 'down' and self.countdown > 0:
            # On completion of the countdown, call function
            self.anim.bind( on_complete = self.initiate_shutdown )
            # Start the animation
            self.anim.start( self )
            print( 'start_timer; ' + str( self.countdown ) )


    def add_time( self, button_time ):
        print( 'add_time() called' )
        self.start_stop_timer()
        self.countdown += button_time
        self.start_stop_timer()


    def sub_time( self, button_time ):
        print( 'sub_time() called; ' + self.ids.start_pause.state + '; ' + str( self.countdown ) )
        if button_time >= self.countdown:
            if self.ids.start_pause.state == 'down':
                self.toggle_add_time_status()
                self.sub_time_disabled = True
                Animation.cancel_all( self )
                self.im_popup.open()
            else:
                self.countdown = 0
                self.sub_time_disabled = True
        else:
            self.start_stop_timer()
            self.countdown -= button_time
            self.start_stop_timer()


    def popup_yes( self ):
        print( 'popup_yes() called' )
        self.countdown = 0
        self.initiate_shutdown()
        self.final_popup.start_final_timer()


    def popup_no( self ):
        print( 'popup_no() called' )
        self.anim.start( self )
        self.toggle_add_time_status()
        self.sub_time_disabled = False


    def reset( self ):
        print( 'reset() called' )
        Animation.cancel_all( self ), self.clear_timer(), self.toggle_start_pause_status(), self.toggle_start_pause_text(), self.toggle_start_pause_state(), self.toggle_preset_status(), self.toggle_sub_time_status(), self.toggle_abort_status(), self.toggle_preset_state()



class TestWinShutdown_v1_1App( App ):
    def build( self ):
        shutdown_timer = TestWinShutdownTimer()
        return shutdown_timer



#Instantiate top-level/root widget and run it
if __name__ == "__main__":
    TestWinShutdown_v1_1App().run()
