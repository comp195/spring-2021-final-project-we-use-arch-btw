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

if __name__ == "__main__":
    a = LocalStorageHandler("test.db")
    # In the real deal, better way of implementing check
    if not os.path.isfile("test.db"):
        a.create()
    # Needed to import state here, but not worth cause its such a pain, thus the plaintext
    p1 = "After the devastating events of Avengers: Infinity War (2018), the universe is in ruins. With the help of remaining allies, the Avengers assemble once more in order to reverse Thanos' actions and restore balance to the universe."
    a.saveToDB("tt4154796", "Avengers: Endgame", "2019", "PG-13", "Action, Adventure, Drama, Sci-Fi",
               p1, None, "94%", "/home/user/Desktop/avengers.mp4", "181 min", 'WATCHED', 2)
