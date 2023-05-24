from watchdog.events import FileSystemEventHandler
from src.databaseInteractor import DatabaseInteractor


class Handler(FileSystemEventHandler):

    def __init__(self, interactor: DatabaseInteractor):
        self.interactor = interactor

    def on_any_event(self, event):
        self.interactor.syncSongLibrary()
