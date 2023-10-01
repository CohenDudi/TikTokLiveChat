from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': ["TikTokLive" , ], 'excludes': []}

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('gametest.py', base=base)
]

setup(name='tikTokLiveChat',
      version = '1',
      description = 'game with chat',
      options = {'build_exe': build_options},
      executables = executables)
