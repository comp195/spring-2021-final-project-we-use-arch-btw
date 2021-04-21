from LVL.Media.media import Media
import sqlite3
import os.path
import os
from LVL import get_data_file # pylint: disable=import-error


class LocalStorageHandler:

    def __init__(self, dbPath = None):
        if dbPath is None:
            self.dbPath = os.path.join(get_data_file('lvl.db'))
        else:
            self.dbPath = dbPath
        self.connection: sqlite3.Connection = None
        self.cursor: sqlite3.Cursor = None

    def initialize_database(self):
        print(f"Initializing database at {self.dbPath}")
        if not os.path.exists(self.dbPath):
            os.makedirs(os.path.dirname(self.dbPath), exist_ok=True)
        self.connection = sqlite3.connect(self.dbPath)
        self.cursor = self.connection.cursor()
        self.create()

    # For when there's no file there
    def create(self):
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS MOVIE (
                imdbId TEXT PRIMARY KEY NOT NULL,
                title TEXT,
                year TEXT,
                rating TEXT,
                genre TEXT,
                plot TEXT,
                poster TEXT,
                rottenTomatoesRating TEXT,
                filePath TEXT NOT NULL,
                duration TEXT NOT NULL,
                state TEXT NOT NULL,
                playCount INT NOT NULL
            )'''
        )

    def save_to_db(self, imdbID, title, year, rating, genre, plot, poster, rottonTomatoesRating, filePath, duration, state, playCount):
        # This will break if we try to insert something into it twice
        self.cursor.execute(
            '''INSERT INTO MOVIE VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )''', (imdbID, title, year, rating, genre, plot, poster, rottonTomatoesRating, filePath, duration, state, playCount,)
        )
        self.connection.commit()
    
    def update_in_db(self, media: Media):
        self.cursor.execute(
            """UPDATE MOVIE SET title = ?, year = ?, rating = ?, genre = ?, plot = ?, poster = ?, 
            rottenTomatoesRating = ?, filePath = ?, duration = ?, state = ?, playCount = ? WHERE imdbId = ?""", 
        media.title, media.year, media.rating, media.genre, media.plot, media.poster, media.rottenTomatoesRating, media.filePath, media.duration, media.state, media.playCount, media.imdbID)
        self.connection.commit()
        pass
