from LVL.Media.media import Media   #  Pylint in vsc doesn't like this for some reason... pylint: disable=import-error
from LVL.Media.state import State   #  Pylint in vsc doesn't like this for some reason... pylint: disable=import-error
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
                rottenTomatoesRating TEXT,
                filePath TEXT NOT NULL,
                duration TEXT NOT NULL,
                state TEXT NOT NULL,
                playCount INT NOT NULL
            )'''
        )

    def save_to_db(self, imdbID, title, year, rating, genre, plot, rottonTomatoesRating, filePath, duration, state, playCount):
        try:
            self.cursor.execute(
                '''INSERT INTO MOVIE VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )''', (imdbID, title, year, rating, genre, plot, rottonTomatoesRating, filePath, duration, state, playCount,)
            )
            self.connection.commit()
        except sqlite3.IntegrityError:
            print("Existing Movie in DB, skipping.")
    
    def save_media_to_db(self, media: Media):
        return self.save_to_db(media.imdbID, media.title, media.year, media.rating, media.genre, media.plot, media.rottenTomatoesRating, media.filePath, media.duration, media.state.value, media.playCount)

    def update_in_db(self, media: Media):
        self.cursor.execute(
            """UPDATE MOVIE SET title = ?, year = ?, rating = ?, genre = ?, plot = ?, rottenTomatoesRating = ?,
             filePath = ?, duration = ?, state = ?, playCount = ? WHERE imdbId = ?""", 
        [media.title, media.year, media.rating, media.genre, media.plot, media.rottenTomatoesRating, media.filePath, media.duration, media.state.name, media.playCount, media.imdbID])
        self.connection.commit()
        pass
    
    def retrieve_from_db(self, imdbID):
        cursor = self.connection.execute(
            """Select * from Movie WHERE MOVIE.imdbid = ?""",
            [imdbID])
        for row in cursor:
            m = Media(row[0],   # imdbID
                    row[1],     # title
                    row[2],     # year
                    row[3],     # rating
                    row[4],     # genre
                    row[5],     # plot
                    row[6],     # rottomTomatoesRating
                    row[7],     # File Path
                    row[8],     # Duration
                    State(row[9]),    # State
                    row[10])    # Play Count
        return(m)
        
    
    def retrieve_all_from_db(self):
        cursor = self.connection.execute(
            """Select * from Movie""")
        m_list = []
        for row in cursor:
            m = Media(row[0],   # imdbID
                    row[1],     # title
                    row[2],     # year
                    row[3],     # rating
                    row[4],     # genre
                    row[5],     # plot
                    row[6],     # rottomTomatoesRating
                    row[7],     # File Path
                    row[8],     # Duration
                    State(row[9]),    # State
                    row[10])    # Play Count
            m_list.append(m)
        return(m_list)