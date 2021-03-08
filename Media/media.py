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

