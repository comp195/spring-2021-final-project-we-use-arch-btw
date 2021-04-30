# pylint: disable=no-member
from pkg_resources import resource_filename
from LVL.threading import AsyncCall
from LVL.LocalStorageHandler.poster_handler import download_poster
from LVL.LocalStorageHandler.handler import LocalStorageHandler
from re import search
from LVL.UI.search import SearchWindow
from LVL.Media.media import Media
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

import os

@Gtk.Template(filename=resource_filename(__name__, "bulk_import_dialog.ui"))
class BulkImport(Gtk.Window):

    __gtype_name__ = "BulkImportDialog"

    entry_list = Gtk.Template.Child()

    def __init__(self, autodetected_media, handler: LocalStorageHandler) -> None:
        super().__init__()
        
        self.built_entries = {}
        self.autodetected_media = autodetected_media
        self.populate_entries()
        self.search_window = None
        self.handler = handler


    def populate_entries(self):
        # Remove the old children
        for row in self.entry_list.get_children():
            self.entry_list.remove(row)
        # Maybe auto close the dialog if the last item is removed?
        for entry in self.autodetected_media:
            self.built_entries[entry] = self.make_entry(entry)
            self.entry_list.add(self.built_entries[entry])
    
    def make_entry(self, media: Media):
        builder = Gtk.Builder()
        builder.add_from_file(resource_filename(__name__, "bulk_import_entry.ui"))

        box = builder.get_object('movie_entry')
        box.show()

        movie_name = builder.get_object('movie_name')
        movie_path = builder.get_object('file_path')
        movie_name.set_text(f"{media.title} ({media.year})")
        movie_path.set_text(media.filePath)

        # Buttons
        remove_button = builder.get_object('remove_button')
        edit_button = builder.get_object('edit_button')
        remove_button.connect('clicked', self.on_remove, media)
        edit_button.connect('clicked', self.on_edit, media)

        return box

    def on_remove(self, _widget, media):
        print(f"Removing {media}")
        self.autodetected_media.remove(media)
        self.populate_entries()
    
    def on_edit(self, _widget, media: Media):
        print(f"Editing media {media}")
        def teardown_search(_widget):
            self.search_window = None
        def search_callback(_widget, m):
            print(f"Running search callback")
            new_media = m.media
            # Replace the stuff we've already got
            for i in range(0, len(self.autodetected_media)):
                if self.autodetected_media[i].imdbID == media.imdbID:
                    self.autodetected_media[i] = new_media
                    break
            self.populate_entries()
            if self.search_window is not None:
                print("Tearing down search")
                self.search_window.destroy()
        # Bring up the search box
        if self.search_window is None:
            self.search_window = SearchWindow(media.title, media.filePath)
            self.search_window.present()
            self.search_window.connect('media-selected', search_callback)
            self.search_window.connect('destroy', teardown_search)

    @Gtk.Template.Callback('confirm_button')
    def do_import(self, _widget):
        print(f"Importing new media")
        _FinalImportDialog(self.autodetected_media, self.handler).run()
        self.destroy()


class _FinalImportDialog(Gtk.Dialog):

    def __init__(self, media, handler: LocalStorageHandler) -> None:
        super().__init__()
        self.set_size_request(320, 60)
        self.set_border_width(24)
        self.set_title("Importing Movies")
        # self.set_decorated(False)
        vbox = Gtk.Box.new(Gtk.Orientation.VERTICAL, 12)
        self.label = Gtk.Label("Importing Movies")
        vbox.add(self.label)
        self.progress = Gtk.ProgressBar(visible=True)
        self.progress.set_pulse_step(0.1)
        vbox.add(self.progress)
        self.get_content_area().add(vbox)
        self.pulse_timeout = GLib.timeout_add(125, self.show_progress)
        self.show_all()

        self.media = media
        self.handler = handler

        self.autodetected_media = []

        AsyncCall(self.import_movies, self.callback)

    def show_progress(self):
        self.progress.pulse()
        return True

    def callback(self, *args, **kwargs):
        self.destroy()

    def import_movies(self):
        for media in self.media:
            def save():
                self.handler.save_media_to_db(media)
            GLib.idle_add(save)
            download_poster(media.imdbID)
