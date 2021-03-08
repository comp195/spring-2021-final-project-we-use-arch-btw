from state import State


class Media:

    def __init__(self, imdbID, title, year, rating, genre, plot, poster, rottenTomatoesRating, filePath, duration, state, playCount):
        # Below: grabbed from OMDBAPI
        self.imdbID = imdbID
        self.title = title
        self.year = year
        self.rating = rating
        self.genre = genre
        self.plot = plot
        self.poster = poster  # B64 encode of image
        self.rottenTomatoesRating = rottenTomatoesRating
        # Below: grabbed from the user's file
        self.filePath = filePath
        self.duration = duration
        # Below: input by user/impacted by gui
        self.state = state  # Enum of WATCHED, IN_PROGRESS, or UNWATCHED
        self.playCount = playCount

    def __str__(self):
        return f'''
        IMDBID: {self.imdbID}
        Title: {self.title}
        Year: {self.year}
        Rating: {self.rating}
        Genre: {self.genre}
        Plot:
        \t{self.plot}
        Poster (B64): {self.poster}
        Rotten Tomatoes Rating: {self.rottenTomatoesRating}
        File Path: {self.filePath}
        Duration: {self.duration}
        State: {self.state.name}
        Play Count: {self.playCount}'''

    def markUnwatched(self):
        self.state = State.UNWATCHED
        self.playCount = 0  # Do we want/need this?
        # TODO Update in DB

    def markWatched(self):
        self.state = State.WATCHED
        # TODO Update in DB

    def incrementPlayCount(self):
        self.markWatched()
        self.playCount += 1
        # TODO Update in DB


if __name__ == "__main__":
    # Temp dummy data manually grabbed from OMDBAPI to test printing
    p1 = "After the devastating events of Avengers: Infinity War (2018), the universe is in ruins. With the help of remaining allies, the Avengers assemble once more in order to reverse Thanos' actions and restore balance to the universe."
    m1 = Media("tt4154796", "Avengers: Endgame", "2019", "PG-13", "Action, Adventure, Drama, Sci-Fi",
               p1, None, "94%", "/home/user/Desktop/avengers.mp4", "181 min", State.WATCHED, 2)
    print(m1)
    m1.markUnwatched()
    print(m1)
    m1.markWatched()
    print(m1)
    m1.incrementPlayCount()
    m1.incrementPlayCount()
    m1.incrementPlayCount()
    print(m1)
