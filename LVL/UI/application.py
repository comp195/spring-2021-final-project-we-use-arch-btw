# pylint: disable=no-member
# --- GTK Initialization ---
import os
from re import search
import sys
import gi
gi.require_version("Gtk", "3.0")
gi.require_version('GdkPixbuf', '2.0')
# --- End GTK Initialization ---
from gi.repository import Gio, Gtk, GdkPixbuf, Gdk

from fuzzywuzzy import process
from LVL.Media.media import Media
from LVL.Media.state import State
from LVL.UI.media import MediaDetails
from LVL.LocalStorageHandler.poster_handler import get_poster_file
from LVL.LocalStorageHandler.handler import LocalStorageHandler


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
    
    @Gtk.Template.Callback("add_media")
    def show_add_media(self, widget):
        file_picker = Gtk.FileChooserDialog("Select a folder", self,
                                       Gtk.FileChooserAction.SELECT_FOLDER,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        response = file_picker.run()
        if response == Gtk.ResponseType.OK:
            print(f"Open clicked {file_picker.get_filename()}")
            # TODO: hook this up to the media backend
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
        self.media_ui.present()
    
    def on_edit_show(self, widget):
        self._load_persistant_media()
        self.load_posters()

    def _load_media_posters(self):
        self.media_gobjects = {}
        for m in self.media:
            self.media_gobjects[m.imdbID] = GdkPixbuf.Pixbuf.new_from_file_at_size(get_poster_file(m.imdbID), 50, 75)

    def _load_temporary_media(self):
        temp_poster_path = os.path.join(os.path.dirname(__file__), "temp_posters")
        media = [
            [
                'tt4154796',
                'Avengers: Endgame',
                '2019',
                'PG13',
                'Action, Adventure, Drama',
                'The plot',
                os.path.join(temp_poster_path, 'Avengers: Endgame.jpg'),
                'N/A',
                '~/Movies/endgame.mp4',
                '',
                 State.UNWATCHED,
                0
            ],
            [
                'tt0368226',
                'The Room',
                '2003',
                'R',
                'Drama',
                'Johnny is a successful bank executive who lives quietly in a San Francisco townhouse with his fiancée, Lisa. One day, putting aside any scruple, she seduces Johnny\'s best friend, Mark. From there, nothing will be the same again. ',
                os.path.join(temp_poster_path, 'The Room.jpg'),
                'N/A',
                '~/Movies/room.mp4',
                '',
                State.UNWATCHED,
                0
            ],
            [
                'tt1285016',
                'The Social Network',
                '2010',
                'PG-13',
                'Drama, Biography',
                'The plot',
                os.path.join(temp_poster_path, 'The Social Network.jpg'),
                'N/A',
                '~/Movies/social_network.mp4',
                '',
                State.UNWATCHED,
                30
            ]
        ]
        for m in media:
            self.media.append(Media(*m))

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
