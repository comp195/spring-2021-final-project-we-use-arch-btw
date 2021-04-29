# pylint: disable=no-member
from LVL.Media.state import State
import gi
gi.require_version("Gtk", "3.0")
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import Gio, Gtk, GdkPixbuf, Gdk
import os
from re import search
import sys
from LVL.Media.media import Media
from LVL.LocalStorageHandler.handler import LocalStorageHandler
from LVL.LocalStorageHandler.poster_handler import get_poster_file
from LVL.UI.edit import EditWindow


@Gtk.Template(filename=os.path.join(os.path.dirname(__file__), "media.ui"))
class MediaDetails(Gtk.Window):

    __gtype_name__ = "MediaWindow"

    media_title = Gtk.Template.Child()
    media_year = Gtk.Template.Child()
    media_poster = Gtk.Template.Child()
    media_information = Gtk.Template.Child()
    delete_confirm = Gtk.Template.Child()
    play_button = Gtk.Template.Child()

    def __init__(self, media: Media, application, handler: LocalStorageHandler):
        super().__init__(application=application)
        self.media = media
        self.application = application
        self.local_storage_handler = handler
        self.edit_window = None

        self.populate_ui(media)

    def populate_ui(self, media):
        self.media_title.props.label = media.title
        self.media_year.props.label = media.year
        self.poster_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(get_poster_file(media.imdbID), 300, 400)
        self.media_poster.props.pixbuf = self.poster_pixbuf

        self.text_buff = Gtk.TextBuffer()
        self.text_buff.props.text = f"{media.plot}\n\nRated: {media.rating}\nGenre: {media.genre}\nRotten Tomatoes: {media.rottenTomatoesRating}\nPlay Count: {media.playCount}\n\n{State.make_human_readable(media.state)}"
        self.media_information.props.buffer = self.text_buff

        # Disable the play button if the file doesn't exist
        if not os.path.exists(self.media.filePath):
            self.play_button.props.opacity = 0.5
            self.play_button.props.can_focus = False
            self.play_button.props.sensitive = False
            self.play_button.props.tooltip_text = "Media file not found"


    @Gtk.Template.Callback("edit_button_clicked")
    def on_edit_click(self, widget):
        if self.edit_window is not None:
            self.edit_window.destory()
        self.edit_window = EditWindow(self.media, self.application, self.local_storage_handler)
        self.edit_window.present()
        self.hide()
        self.edit_window.connect('destroy', self.on_edit_close)
    
    def on_edit_close(self, widget):
        self.edit_window = None
        # Update the view screen
        self.media = self.local_storage_handler.retrieve_from_db(self.media.imdbID)
        self.populate_ui(self.media)
        self.show()

    @Gtk.Template.Callback("play_button_clicked")
    def on_play_button_click(self, widget):
        print("Opening the media player!")

    @Gtk.Template.Callback("delete_button_clicked")
    def delete_button_clicked(self, widget):
        self.delete_confirm.show()
        self.delete_confirm.connect('destroy', self.on_delete_confirm_exit)

    def on_delete_confirm_exit(self, widget):
        if self.delete_confirm:
            self.delete_confirm.hide()

    @Gtk.Template.Callback("click_yes")
    def delete_confirmed(self, widget):
        self.local_storage_handler.delete(self.media.imdbID)
        self.delete_confirm.hide()
        self.destroy()

    @Gtk.Template.Callback("click_no")
    def click_no(self, widget):
        if self.delete_confirm:
            self.delete_confirm.hide()
