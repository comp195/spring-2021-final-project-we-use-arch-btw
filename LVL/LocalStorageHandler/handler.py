import sqlite3
import os.path


class LocalStorageHandler:

    def __init__(self, dbPath):
        self.dbPath = dbPath
        self.connection = sqlite3.connect(dbPath)
        self.cursor = self.connection.cursor()

    # For when there's no file there
    def create(self):
        self.cursor.execute(
            '''CREATE TABLE MOVIE (
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

