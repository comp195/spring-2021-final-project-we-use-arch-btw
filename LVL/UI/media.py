# pylint: disable=no-member
import gi
gi.require_version("Gtk", "3.0")
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import Gio, Gtk, GdkPixbuf, Gdk
import os
from re import search
import sys
from LVL.Media.media import Media


@Gtk.Template(filename=os.path.join(os.path.dirname(__file__), "media.ui"))
class MediaDetails(Gtk.Window):

    __gtype_name__ = "MediaWindow"

    media_title = Gtk.Template.Child()
    media_year = Gtk.Template.Child()
    media_poster = Gtk.Template.Child()
    media_information = Gtk.Template.Child()

    def __init__(self, media: Media, application):
        super().__init__(application=application)
        self.media_title.props.label = media.title
        self.media_year.props.label = f"<i>{media.year}</i>"
        self.poster_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(media.poster, 300, 400)
        self.media_poster.props.pixbuf = self.poster_pixbuf

        self.text_buff = Gtk.TextBuffer()
        self.text_buff.props.text = f"{media.plot}\n\nRated: {media.rating}\nGenre: {media.genre}"
        self.media_information.props.buffer = self.text_buff

