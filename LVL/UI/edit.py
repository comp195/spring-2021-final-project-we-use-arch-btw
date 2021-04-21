# pylint: disable=no-member
from LVL.Media.media import Media
import gi
gi.require_version("Gtk", "3.0")
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import Gio, Gtk, GdkPixbuf, Gdk
import os
from re import search
import sys


@Gtk.Template(filename=os.path.join(os.path.dirname(__file__), "edit.ui"))
class EditWindow(Gtk.Window):
    
    __gtype_name__ = "EditWindow"

    title_box = Gtk.Template.Child()
    year_box = Gtk.Template.Child()
    genre_box = Gtk.Template.Child()
    rating_box = Gtk.Template.Child()
    actors_box = Gtk.Template.Child()
    plot_box = Gtk.Template.Child()
    poster_image = Gtk.Template.Child()

    def __init__(self, media: Media, application):
        super().__init__(application=application)

        self.title_box.props.text = media.title
        self.year_box.props.text = media.year
        self.genre_box.props.text = media.genre
        self.rating_box.props.text = media.rating
        self.plot_box.props.text = media.plot

        self.poster_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(media.poster, 300, 400)
        self.poster_image.props.pixbuf = self.poster_pixbuf
    
    @Gtk.Template.Callback("save")
    def save_media(self, widget):
        print("Saving the media")
        pass

    @Gtk.Template.Callback("cancel")
    def cancel_edit(self, widget):
        self.destroy()