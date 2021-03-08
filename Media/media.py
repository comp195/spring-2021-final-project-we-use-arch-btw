class Media:

    def __init__(self):
        self.title = ''
        self.year = ''
        self.rating = ''
        self.genre = ''
        self.plot = ''
        self.poster = ''  # B64 encode of image
        self.rottenTomatoesRating = ''
        self.filePath = ''
        self.duration = ''
        self.state = None  # Enum of WATCHED, IN_PROGRESS, or UNWATCHED
        self.playCount = 0

    def __str__(self: Media):
        return f'''
        Title: {self.title}
        Year: {self.year}
        Rating: {self.rating}
        Genre: {self.genre}
        Plot:
        {self.plot}
        Poster (B64): {self.poster}
        Rotton Tomatoes Rating: {self.rottenTomatoesRating}
        File Path: {self.filePath}
        Duration: {self.duration}
        State: {self.state}
        Play Count: {self.playCount}
        '''
