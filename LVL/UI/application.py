# pylint: disable=no-member
# --- GTK Initialization ---
import os
from re import search
import sys
import gi
gi.require_version("Gtk", "3.0")
gi.require_version('GdkPixbuf', '2.0')
# --- End GTK Initialization ---
from gi.repository import Gio, Gtk, GdkPixbuf, Gdk, GLib

from fuzzywuzzy import process
from LVL.Media.media import Media
from LVL.Media.state import State
from LVL.UI.media import MediaDetails
from LVL.UI.search import SearchWindow
from LVL.LocalStorageHandler.poster_handler import get_poster_file, download_poster
from LVL.LocalStorageHandler.handler import LocalStorageHandler
from LVL.LocalStorageHandler.media_title_parser import parse_file
from LVL.omdbapi import omdb_search, omdb_get, parse_result
from LVL.threading import AsyncCall
from LVL import show_error_dialog

class BuklImportDialog(Gtk.Dialog):

    def __init__(self, path: str, handler: LocalStorageHandler) -> None:
        super().__init__()
        self.set_size_request(320, 60)
        self.set_border_width(24)
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

        self.processed_movies = 0
        self.total_movies = 0
        self.path = path
        self.handler = handler

        AsyncCall(self.import_movies, self.callback)
    
    def show_progress(self):
        self.progress.pulse()
        return True
    
    def update_progress_bar(self):
        if self.total_movies < 0:
            return
        if self.pulse_timeout is not None:
            GLib.source_remove(self.pulse_timeout)
            self.pulse_timeout = None
        progress = self.processed_movies / self.total_movies
        self.label.props.label = f"Importing Movies ({self.processed_movies} / {self.total_movies})"
        self.progress.props.fraction = progress

    def import_movies(self):
        print(f"Importing movies from {self.path}")
        media_files = []
        failed_files = []
        for root, _, files in os.walk(self.path):
            for name in files:
                print(f"Found file {os.path.join(root, name)}")
                media_files.append(os.path.join(root, name))
        self.total_movies = len(media_files)
        for media_file in media_files:
            parsed = parse_file(media_file)
            print(f"{media_file} = {parsed}")
            if parsed is None:
                print(f"Could not import {media_file}")  # This should also be a dialog box
                continue
            try:
                omdb_data = omdb_get(parsed.imdb_id) if parsed.imdb_id is not None else omdb_search(
                    parsed.name, parsed.year)
                new_media_obj = parse_result(omdb_data)
                new_media_obj.filePath = media_file
                download_poster(new_media_obj.imdbID)
                GLib.idle_add(self.handler.save_media_to_db, new_media_obj)
            except:
                failed_files.append(media_file)
                
            self.processed_movies += 1
            GLib.idle_add(self.update_progress_bar)
        
        if len(failed_files) > 0:
            self.hide()
            fail_text = '\n'.join(failed_files)
            show_error_dialog(self, f"The following files could not be imported:\n{fail_text}")
    
    def callback(self, _result, error):
        self.destroy()

@Gtk.Template(filename=os.path.join(os.path.dirname(__file__), "main.ui"))
class LVLWindow(Gtk.ApplicationWindow):
    __gtype_name__ = "LVLWindow"

    posters = Gtk.Template.Child()
    search_entry = Gtk.Template.Child()

    def __init__(self, handler: LocalStorageHandler, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.about_dialog = None
        self.media = []
        self.media_gobjects = {}
        self.search_query = ""
        self.media_ui = None
        self.api_search_window = None
        self.application = kwargs['application']

        self.local_storage_handler = handler
    
        # Temporarily load some media
        # Uncomment to use temp media, real is below
        # self._load_temporary_media()

        # Load media from database
        self._load_persistant_media()

        self.load_posters()

    def load_posters(self):
        # Cache the list of posters
        self._load_media_posters()

        self.media_liststore = Gtk.ListStore(GdkPixbuf.Pixbuf, str, str) # Image, Title, IMDB ID
        self.posters.set_model(self.media_liststore)
        self.posters.set_pixbuf_column(0)
        self.posters.set_text_column(1)
        self.posters.connect('selection-changed', self.on_media_select)
        self.update_search()

    @Gtk.Template.Callback("about_clicked")
    def about_clicked(self, widget):
        if not self.about_dialog:
            self.about_dialog = Gtk.AboutDialog(
                program_name="Local Video Library",
                version="1.0",
                authors=["Austin Whyte", "Alex Reynen"]
            )
            self.about_dialog.connect("close", self.close_about)
            self.about_dialog.connect("response", self.close_about)
        self.about_dialog.show()
        pass
    
    @Gtk.Template.Callback("add_single_media")
    def add_single_media(self, widget):
        file_picker = Gtk.FileChooserDialog("Select a File", self,
                                       Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        response = file_picker.run()
        if response == Gtk.ResponseType.OK:
            selection = file_picker.get_filename()
            parsed = parse_file(selection)
            print(f"{selection} = {parsed}")
            if self.api_search_window is not None:
                self.api_search_window.hide()
            print(parsed)
            name = parsed.name if parsed is not None else os.path.splitext(os.path.basename(selection))[0]
            self.api_search_window = SearchWindow(name, selection,  self.application, self.local_storage_handler)
            file_picker.destroy()
            self.api_search_window.present()
            self.api_search_window.connect('destroy', self.close_search_window)
        else:
            file_picker.destroy()

    def close_search_window(self, widget):
        self.api_search_window = None
        self._load_persistant_media()
        self._load_media_posters()
        self.update_search()

    @Gtk.Template.Callback("add_media")
    def show_add_media(self, widget):
        file_picker = Gtk.FileChooserDialog("Select a Folder", self,
                                       Gtk.FileChooserAction.SELECT_FOLDER,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        response = file_picker.run()
        if response == Gtk.ResponseType.OK:
            path = file_picker.get_filename()
            file_picker.destroy()
            print(f"Open clicked {path}")
            BuklImportDialog(path, self.local_storage_handler).run()
            self._load_persistant_media()
            self._load_media_posters()
            self.update_search()
        else:
            file_picker.destroy()
    
    @Gtk.Template.Callback("search_change")
    def search_change(self, widget):
        self.search_query = widget.props.text
        self.update_search()
        pass

    def do_key_press_event(self, event):
        if event.keyval == Gdk.KEY_Escape:
            self.search_entry.set_text("")
            self.search_query = ""
            self.update_search()
        return Gtk.ApplicationWindow.do_key_press_event(self, event)
    
    def update_search(self):
        if self.search_query != "":
            self.media_liststore.clear()
            search_dictionary = {}
            for m in self.media:
                search_dictionary[m.imdbID] = m.title
            ranked = process.extract(self.search_query, search_dictionary)
            for title, score, id in ranked:
                if score < 50:
                    continue
                self.media_liststore.append([self.media_gobjects[id], title, id])
        else:
            self.media_liststore.clear()
            for m in self.media:
                poster = self.media_gobjects[m.imdbID]
                self.media_liststore.append([poster, m.title, m.imdbID])

    def close_about(self, *args):
        if self.about_dialog:
            self.about_dialog.hide()
    
    def on_media_select(self, iconview):
        selected = iconview.get_selected_items()
        if len(selected) > 0:
            selected = selected[0]
            value = self.media_liststore.get_value(self.media_liststore.get_iter(selected), 2)
            print(f"Opening media dialog for {value}")
            for m in self.media:
                if m.imdbID == value:
                    self.open_media_dialog(m)
        iconview.unselect_all()

    def open_media_dialog(self, media: Media):
        if self.media_ui is not None:
            # Swap from destroy media_ui to exiting, so we cant have a media + edit at once
            # self.media_ui.destroy()
            return
        self.media_ui = MediaDetails(media, self.application, self.local_storage_handler)
        self.media_ui.connect('show', self.on_edit_show)
        self.media_ui.connect('destroy', self.on_media_exit)
        self.media_ui.present()
    
    def on_edit_show(self, widget):
        self._load_persistant_media()
        self.load_posters()

    def on_media_exit(self, widget):
        self.media_ui = None
        self._load_persistant_media()
        self.load_posters()

    def _load_media_posters(self):
        self.media_gobjects = {}
        for m in self.media:
            self.media_gobjects[m.imdbID] = GdkPixbuf.Pixbuf.new_from_file_at_size(get_poster_file(m.imdbID), 50, 75)

    def _load_persistant_media(self):
        self.media = []
        media = self.local_storage_handler.retrieve_all_from_db()
        for m in media:
            self.media.append(m)


class Application(Gtk.Application):
    def __init__(self, storage_handler: LocalStorageHandler):
        super().__init__(
            application_id="com.github.lvl",
            flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE
        )
        self.storage_handler = storage_handler
        self.window = None

    def do_startup(self):
        Gtk.Application.do_startup(self)

        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.on_quit)
        self.add_action(action)

    def do_activate(self):
        if not self.window:
            self.window = LVLWindow(self.storage_handler, application=self)
        self.window.present()

    def do_command_line(self, command_line):
        options = command_line.get_options_dict()
        # convert GVariantDict -> GVariant -> dict
        options = options.end().unpack()

        self.activate()
        return 0

    def on_quit(self, action, param):
        self.quit()
