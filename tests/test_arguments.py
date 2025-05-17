import sys
import types
import importlib
import pytest


def load_import_spotify(monkeypatch):
    """Load import_spotify with stubbed spotipy module."""
    spotipy_stub = types.ModuleType("spotipy")
    oauth2_stub = types.ModuleType("spotipy.oauth2")

    class DummySpotifyOAuth:
        def __init__(self, *args, **kwargs):
            pass

    oauth2_stub.SpotifyOAuth = DummySpotifyOAuth
    spotipy_stub.oauth2 = oauth2_stub

    monkeypatch.setitem(sys.modules, "spotipy", spotipy_stub)
    monkeypatch.setitem(sys.modules, "spotipy.oauth2", oauth2_stub)

    return importlib.import_module("import_spotify")


def test_missing_playlist(monkeypatch):
    module = load_import_spotify(monkeypatch)
    monkeypatch.setattr(sys, "argv", ["import_spotify.py", "--csv", "songs.csv"])
    with pytest.raises(SystemExit):
        module.parse_arguments()


def test_missing_csv(monkeypatch):
    module = load_import_spotify(monkeypatch)
    monkeypatch.setattr(sys, "argv", ["import_spotify.py", "--playlist", "MyList"])
    with pytest.raises(SystemExit):
        module.parse_arguments()


def test_parse_arguments_success(monkeypatch):
    module = load_import_spotify(monkeypatch)
    monkeypatch.setattr(
        sys,
        "argv",
        ["import_spotify.py", "--playlist", "MyList", "--csv", "songs.csv"],
    )
    args = module.parse_arguments()
    assert args.playlist == "MyList"
    assert args.csv == "songs.csv"
