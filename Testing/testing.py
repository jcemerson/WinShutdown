# Set .kivy\config.ini > graphics > multisamples to '0' (for this instance only) in order to prevent "black screen":
from kivy import Config
Config.set( 'graphics', 'multisamples', 0 )
Config.set( 'graphics', 'fullscreen', 0 )
Config.set( 'graphics', 'height', 300 )
Config.set( 'graphics', 'width', 400 )
Config.set( 'graphics', 'resizable', 0 )

# # Slider Testing:
# from kivy.uix.slider import Slider
# s = Slider(value_track=True, value_track_color=[1, 0, 0, 1])


# # Getting a list of IDs from Properties:
# ids = {'A': 'set20', 'B': 'set40', 'C': 'stuff60' }
# tblist = []
# for v in ids.values():
#     if v.startswith( 'set' ):
#         tblist.append( v )
# print( tblist )


from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

from kivy.config import Config
Config.set('kivy', 'exit_on_escape', '0')

class KeyDown(App):
    def build(self):
        self.popup_exists = 0
        Window.bind(on_key_down=self.key_action)
        return Widget()

    def key_action(self, *args):
        key1 = args[1]
        key2 = args[2]
        special_keys = args[4]
        letter = args[3]

        if special_keys == ['ctrl'] and letter == 'f':                          # Ctrl-F
            print('Find')
            self.open_find_dialog()
        if key1 == 13 and key2 == 40 and self.popup_exists == 1:                # ENTER KEY
            pass
        if key1 == 27 and key2 == 41 and self.popup_exists == 1:    # ESC
            self.find_window.dismiss()

    def open_find_dialog(self):
        content = BoxLayout(orientation='horizontal')
        col1_cont = BoxLayout(size_hint_x = 2,orientation = 'vertical')
        col2_cont = BoxLayout(size_hint_x = 4,orientation = 'vertical')
        find_labl = Label(text='Find',size_hint_y=None, height = 40)
        repl_labl = Label(text='Replace',size_hint_y=None, height = 40)

        find_text = TextInput(text='', size_hint_y = None, height = 40)
        repl_text = TextInput(text='', size_hint_y = None, height = 40)
        col1_cont.add_widget(find_labl)
        col1_cont.add_widget(repl_labl)
        col2_cont.add_widget(find_text)
        col2_cont.add_widget(repl_text)

        content.add_widget(col1_cont)
        content.add_widget(col2_cont)
        self.find_window = Popup(title='Find and Replace',content = content,size_hint=(None, None), size=(240, 140))
        self.find_window.open()
        self.popup_exists = 1
if __name__ == '__main__':
    KeyDown().run()
