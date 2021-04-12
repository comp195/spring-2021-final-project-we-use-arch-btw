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


@Gtk.Template(filename=os.path.join(os.path.dirname(__file__), "main.ui"))
class LVLWindow(Gtk.ApplicationWindow):
    __gtype_name__ = "LVLWindow"

    posters = Gtk.Template.Child()
    search_entry = Gtk.Template.Child()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.about_dialog = None
        self.media = []
        self.media_gobjects = {}
        self.search_query = ""
        self.media_ui = None
        self.application = kwargs['application']

        # Temporarily load some media
        self._load_temporary_media()

        # Cache the list of posters
        self._load_media_posters()

        self.media_liststore = Gtk.ListStore(GdkPixbuf.Pixbuf, str, str) # Image, Title, IMDB ID
        iconview = Gtk.IconView.new()
        iconview.set_model(self.media_liststore)
        iconview.set_pixbuf_column(0)
        iconview.set_text_column(1)
        iconview.connect('selection-changed', self.on_media_select)
        self.posters.add(iconview)
        iconview.show()
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
                    break
        iconview.unselect_all()

    def open_media_dialog(self, media: Media):
        if self.media_ui is not None:
            self.media_ui.destroy()
        self.media_ui = MediaDetails(media, self.application)
        self.media_ui.present()
    
    def _load_media_posters(self):
        for m in self.media:
            self.media_gobjects[m.imdbID] = GdkPixbuf.Pixbuf.new_from_file_at_size(m.poster, 50, 75)

    def _load_temporary_media(self):
        temp_poster_path = os.path.join(os.path.dirname(__file__), "temp_posters")
        media = [
            [
                'tt4154796',
                'Avengers: Endgame',
                '2019',
                '8.4',
                'Action, Adventure, Drama',
                'The plot',
                os.path.join(temp_poster_path, 'Avengers: Endgame.jpg'),
                'N/A',
                '',
                '',
                 State.UNWATCHED,
                0
            ],
            [
                'tt0338621',
                'Kirby: Right Back at Ya!',
                '2001-2003',
                '6.7',
                'Animation, Action, Adventure',
                'The plot',
                os.path.join(temp_poster_path, 'Kirby Right Back At You.jpg'),
                'N/A',
                '',
                '',
                State.UNWATCHED,
                0
            ],
            [
                'tt0368226',
                'The Room',
                '2003',
                '3.7',
                'Drama',
                'The plot',
                os.path.join(temp_poster_path, 'The Room.jpg'),
                'N/A',
                '',
                '',
                State.UNWATCHED,
                0
            ],
            [
                'tt1285016',
                'The Social Network',
                '2010',
                '7.7',
                'Drama, Biography',
                'The plot',
                os.path.join(temp_poster_path, 'The Social Network.jpg'),
                'N/A',
                '',
                '',
                State.UNWATCHED,
                0
            ]
        ]
        for m in media:
            self.media.append(Media(*m))


class Application(Gtk.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            application_id="com.github.lvl",
            flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
            **kwargs
        )
        self.window = None

    def do_startup(self):
        Gtk.Application.do_startup(self)

        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.on_quit)
        self.add_action(action)

    def do_activate(self):
        if not self.window:
            self.window = LVLWindow(application=self)
        self.window.present()

    def do_command_line(self, command_line):
        options = command_line.get_options_dict()
        # convert GVariantDict -> GVariant -> dict
        options = options.end().unpack()

        self.activate()
        return 0

    def on_quit(self, action, param):
        self.quit()
