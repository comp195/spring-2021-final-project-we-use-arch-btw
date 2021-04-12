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

    def __init__(self, media: Media, application):
        super().__init__(application=application)
        self.media_title.props.label = media.title
        self.media_year.props.label = f"<i>{media.year}</i>"
