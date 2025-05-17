import os
import sys
import unittest
from unittest.mock import patch

import types

# Create dummy spotipy module so import_spotify can be imported without the
# real dependency installed.
dummy_spotipy = types.ModuleType('spotipy')
oauth2_mod = types.ModuleType('spotipy.oauth2')

class DummyOAuth:
    def __init__(self, *args, **kwargs):
        pass

    def get_authorize_url(self):
        return 'http://example.com'

    def get_access_token(self, code):
        return {'access_token': 'token'}

dummy_spotipy.oauth2 = oauth2_mod
oauth2_mod.SpotifyOAuth = DummyOAuth

with patch.dict(sys.modules, {'spotipy': dummy_spotipy, 'spotipy.oauth2': oauth2_mod}):
    import import_spotify

class TestEnvVars(unittest.TestCase):
    def test_exit_when_missing_env(self):
        with patch.dict(os.environ, {}, clear=True):
            args = ['import_spotify.py', '--playlist', 'P', '--csv', 'dummy.csv']
            with patch.object(sys, 'argv', args):
                with self.assertRaises(SystemExit) as cm:
                    import_spotify.main()
                self.assertNotEqual(cm.exception.code, 0)

if __name__ == '__main__':
    unittest.main()
