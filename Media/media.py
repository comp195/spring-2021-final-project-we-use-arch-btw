from state import State


class Media:

    def __init__(self, title, year, rating, genre, plot, poster, rottenTomatoesRating, filePath, duration, state, playCount):
        self.title = title
        self.year = year
        self.rating = rating
        self.genre = genre
        self.plot = plot
        self.poster = poster  # B64 encode of image
        self.rottenTomatoesRating = rottenTomatoesRating
        self.filePath = filePath
        self.duration = duration
        self.state = state  # Enum of WATCHED, IN_PROGRESS, or UNWATCHED
        self.playCount = playCount

    def __str__(self):
        return f'''
        Title: {self.title}
        Year: {self.year}
        Rating: {self.rating}
        Genre: {self.genre}
        Plot:
        \t {self.plot}
        Poster (B64): {self.poster}
        Rotton Tomatoes Rating: {self.rottenTomatoesRating}
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
