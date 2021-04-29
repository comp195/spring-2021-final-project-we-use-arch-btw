from gi.repository import GObject
from LVL.Media.media import Media


class MediaGObject(GObject.Object):
    """
    Wrapper class for Media to use in signals
    """

    def __init__(self, media: Media) -> None:
        super().__init__()
        self.media = media
