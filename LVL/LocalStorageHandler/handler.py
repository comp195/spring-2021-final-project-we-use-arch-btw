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

    def saveToDB(self, imdbID, title, year, rating, genre, plot, poster, rottonTomatoesRating, filePath, duration, state, playCount):
        self.cursor.execute(
            '''INSERT INTO MOVIE VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )''', (imdbID, title, year, rating, genre, plot, poster, rottonTomatoesRating, filePath, duration, state, playCount,)
        )
        self.connection.commit()
    
    def updateInDB(self):
        # Some kind of code to say find item based on id, then update the needed thing
        pass
