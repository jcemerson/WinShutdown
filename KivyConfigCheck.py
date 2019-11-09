# Addresses the following issues with Kivy on Windows 10:
# https://github.com/kivy/kivy/issues/5248#issuecomment-370885342

# Enable OS platform and release check
import platform
import subprocess
from kivy import Config

def WindowsCheck():
    # If Windows 10:
    if platform.system() == 'Windows' and platform.release() == '10':
        # Check Windows 10 for appropriate environment variable
        proc = subprocess.Popen(
            'if defined KIVY_GL_BACKEND (echo True) else (echo False)',
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        out, err = proc.communicate()

        # If environment variable KIVY_GL_BACKEND does NOT exist, then
        if out == False:
            # Create environment variable to set KIVY_GL_BACKEND to angle
            # (instead of glew) to prevent issue detecting OpenGL version
            subprocess.call('setx KIVY_GL_BACKEND angle_sdl2', shell=True)
        # Set .kivy\config.ini > graphics > multisamples to '0' (for this instance only)
        # in order to prevent "black screen"
        Config.set('graphics','multisamples', 0)

if __name__ == '__main__':
    WindowsCheck()
