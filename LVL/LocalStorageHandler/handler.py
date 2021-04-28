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
        [media.title, media.year, media.rating, media.genre, media.plot, media.poster, media.rottenTomatoesRating, media.filePath, media.duration, media.state.name, media.playCount, media.imdbID])
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
                    row[6],     # poster
                    row[7],     # rottomTomatoesRating
                    row[8],     # File Path
                    row[9],     # Duration
                    State(row[10]),    # State
                    row[11])    # Play Count
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
                    row[6],     # poster
                    row[7],     # rottomTomatoesRating
                    row[8],     # File Path
                    row[9],     # Duration
                    State(row[10]),    # State
                    row[11])    # Play Count
            m_list.append(m)
        return(m_list)