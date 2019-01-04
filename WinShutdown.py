##### WinShutdown.py v1.0; 01-04-2019 #####
##### Jordan Emerson; WutDuk?         #####
##### https://github.com/jcemerson    #####
###########################################

# NOTE: Updating the countdown during an active countdown is currently not supported.

import KivyConfigCheck
import subprocess
import kivy
from kivy import Config
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.animation import Animation
from kivy.properties import StringProperty, NumericProperty, BooleanProperty, ListProperty
from kivy.uix.slider import Slider

# Supported Kivy version required for operation. Older version may work too, but they're not supported. You can remove or modify this setting at your own risk.
kivy.require( '1.10.1' )

# Script to update settings for Windows 10 issues.
KivyConfigCheck.WindowsCheck()

# Set fixed window size and non-resizable
Config.set( 'graphics', 'fullscreen', 0 )
Config.set( 'graphics', 'height', 600 )
Config.set( 'graphics', 'width', 800 )
Config.set( 'graphics', 'resizable', 0 )
Config.set( 'kivy', 'exit_on_escape', 0 )
Config.set( 'kivy', 'window_icon', '.\Images\power-on.png')



class WinShutdownTimer( GridLayout, ToggleButtonBehavior ):
    # Define default layout and widget attributes
    font_size = 20
    widget_padding = ( 25, 10, 25, 10 )
    spacer_width = 10
    start_pause = StringProperty( 'Start' )
    start_pause_disabled = BooleanProperty( True )
    sub_time_disabled = BooleanProperty( True )
    preset_disabled = BooleanProperty( False )
    abort_disabled = BooleanProperty( True )
    countdown = NumericProperty( 0 )
    abort_background_color = ListProperty( [ 1, 1, 1, 1 ] )

    # Function to set the countdown timer. This doesn't add time. Instead it replaces time.
    def set_timer( self, button_time ):
        # If the countdown is at 0, then
        if self.countdown == 0:
            # Then set the countdown to the time of the button that initiated the call
            self.countdown = button_time

    # Function to clear the timer to 0
    def clear_timer( self ):
        self.countdown = 0

    # Function to toggle the '-15 min' button's state
    def toggle_sub_time_status( self ):
        # If the Start/Pause button is down (i.e., timer countdown is active), then
        if self.ids.start_pause.state == 'down':
            # '-15 min' button is disabled
            self.sub_time_disabled = True
        # Else, if the Start/Pause button is up (i.e., timer is stopped) and countdown is at 0, then
        elif self.ids.start_pause.state == 'normal' and self.countdown == 0:
            # The '-15 min' button is disabled because there's no time to subtract
            self.sub_time_disabled = True
        # Otherwise, the button is active
        else:
            self.sub_time_disabled = False

    # Function to toggle the Start/Pause button status
    def toggle_start_pause_status( self ):
        # If the countdown is greater than 0
        if self.countdown > 0:
            # The Start/Pause button is active and can be clicked
            self.start_pause_disabled = False
        else:
            # Otherwise the timer is at 0 and there's no function for this button, so it's disabled
            self.start_pause_disabled = True

    # Function to toggle the Abort button state
    def toggle_abort_status( self ):
        # If countdown is greater than 0 and the Start/Pause button is down, then
        if self.countdown > 0 and self.ids.start_pause.state == 'down':
            # The Abort button is active, and colored red
            self.abort_disabled = False
            self.abort_background_color = [ 1, 0, 0, 1 ]
        # Else the button is disabled and returns to default gray
        else:
            self.abort_disabled = True
            self.abort_background_color = [ 1, 1, 1, 1 ]

    # Function to toggle the status of preset time buttons (20, 40, 60, 90, 120)
    def toggle_preset_status( self ):
        # If the Start/Pause button is down (countdown is active), then
        if self.ids.start_pause.state == 'down':
            # Then presets are down. To apply a preset, Pause or Abort the countdown.
            self.preset_disabled = True
        # Otherwise they are available and can be selected at any time
        else:
            self.preset_disabled = False

    # Function to toggle the Start/Pause button state (up or down)
    def toggle_start_pause_state( self ):
        # If Start/Pause says 'Start', then
        if self.start_pause == 'Start':
            # Set the button to 'up'
            self.ids.start_pause.state = 'normal'
        # Else the button is down
        else:
            self.ids.start_pause.state = 'down'

    # Function to toggle the state of presets (up or down)
    def toggle_preset_state( self ):
        # If countdown is at 0, the presets are in the 'up' state
        if self.countdown == 0:
            self.ids.set20.state = 'normal'
            self.ids.set40.state = 'normal'
            self.ids.set60.state = 'normal'
            self.ids.set90.state = 'normal'
            self.ids.set120.state = 'normal'

    # Function to toggle the Start/Pause text label of the button
    def toggle_start_pause_text( self ):
        # If the Start/Pause button is down and the countdown is above 0, then
        if self.ids.start_pause.state == 'down' and self.countdown > 0:
            # The countdown is active, so set the button text to 'Pause'
            self.start_pause = 'Pause'
        # Else, set the text to 'Start'
        else:
            self.start_pause = 'Start'


    def initiate_shutdown( self, *args ):
        # Provide the reason for the restart or shutdown. These events are documented as "Other Planned"
        d_cmd = '/d p:0:0'
        # Comment on the reason for the restart or shutdown.
        c_cmd = '/c "Automated User-initiated {cmd} via WinShutdown.py"'
        # build final cmd
        final_cmd = ''
        # If the Start/Pause button is down (should say 'Pause') and the countdown is at 0, then
        if self.ids.start_pause.state == 'down' and self.countdown == 0:
            # If the Shutdown button is down, then
            if self.ids.shutdown.state == 'down':
                # Compile the cmd string for a shutdown
                final_cmd = 'shutdown /s' + ' ' + d_cmd + ' ' + c_cmd.format( cmd = 'Shutdown')
            # Else, if the Restart button is down, then
            elif self.ids.restart.state == 'down':
                # Compile the cmd string for a restart
                final_cmd = 'shutdown /r' + ' ' + d_cmd + ' ' + c_cmd.format( cmd = 'Restart')
            # Else, if the Hibernate button is down, then
            elif self.ids.hibernate.state == 'down':
                # Compile the cmd string for a hibernate
                final_cmd = 'shutdown /h'
            # Else, if none of the above, compile a cmd string for logoff
            else:
                final_cmd = 'shutdown /l'
            # send final cmd to windows cmd shell
            subprocess.call( final_cmd, shell = True )


    def start_stop_timer( self ):
        # Cancel any current animation in progress
        Animation.cancel_all( self )
        # Define the rules for Animation; i.e., ( <where we are going>, <where we're coming from> )
        self.anim = Animation( countdown = 0, duration = self.countdown )
        # on_release of Start/Pause button, if the down and there is still time on the clock, then
        if self.ids.start_pause.state == 'down' and self.countdown > 0:
            # Start the animation
            self.anim.start( self )
            # On completion of the countdown, call function to initiate the shutdown process
            self.anim.bind( on_complete = self.initiate_shutdown )
        # Else, if the button isn't down and there's time on the clock, stop the countdown
        elif self.ids.start_pause.state == 'normal' and self.countdown > 0:
            # Stop the animation
            self.anim.stop( self )

    # Function to add time to the current countdown (as opposed to resetting)
    def add_time( self, button_time ):
        # If the Start/Pause button is 'up', then
        if self.ids.start_pause.state == 'normal':
            # add to the current countdown time the time of the button that initiated the call
            self.countdown += button_time

    # Function to subtract time from the current countdown (as opposed to resetting)
    def sub_time( self, button_time ):
        # If the Start/Pause button is 'up', then
        if self.ids.start_pause.state == 'normal':
            # If the time of the button is greater than the remaining countdown time, instead, just set countdown to 0 rather than a negative time
            if button_time > self.countdown:
                self.countdown = 0
            # Else, subtract the time of the button that initiated the call
            else:
                self.countdown -= button_time

    # Function to reset the entire app when Abort is selected
    def reset( self ):
        self.anim.stop( self ), self.clear_timer(), self.toggle_start_pause_status(), self.toggle_start_pause_text(), self.toggle_start_pause_state(), self.toggle_preset_status(), self.toggle_sub_time_status(), self.toggle_abort_status(), self.toggle_preset_state()


# App class that, when called, instatiates the root class
class WinShutdownApp( App ):
    def build( self ):
        return WinShutdownTimer()



#Instantiate top-level/root widget and run it
if __name__ == "__main__":
    WinShutdownApp().run()
