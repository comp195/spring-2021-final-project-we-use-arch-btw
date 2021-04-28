# pylint: disable=no-member
from LVL.Media.media import Media
from LVL.Media.state import State as WatchState
import gi
gi.require_version("Gtk", "3.0")
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import Gio, Gtk, GdkPixbuf, Gdk, GObject
import os
from re import search
import sys
import tempfile
import shutil
from LVL.LocalStorageHandler.poster_handler import update_poster_file
from LVL.LocalStorageHandler.handler import LocalStorageHandler


@Gtk.Template(filename=os.path.join(os.path.dirname(__file__), "edit.ui"))
class EditWindow(Gtk.Window):
    
    __gtype_name__ = "EditWindow"

    title_box = Gtk.Template.Child()
    year_box = Gtk.Template.Child()
    genre_box = Gtk.Template.Child()
    rating_box = Gtk.Template.Child()
    plot_box = Gtk.Template.Child()
    poster_image = Gtk.Template.Child()
    watch_state = Gtk.Template.Child()
    play_count = Gtk.Template.Child()
    file_path = Gtk.Template.Child()
    rotten_tomatoes = Gtk.Template.Child()

    def __init__(self, media: Media, application, handler: LocalStorageHandler):
        super().__init__(application=application)

        self.media = media
        self.local_storage_handler = handler

        self.title_box.props.text = media.title
        self.year_box.props.text = media.year
        self.genre_box.props.text = media.genre
        self.rating_box.props.text = media.rating
        self.play_count.props.value = media.playCount
        self.rotten_tomatoes.props.text = media.rottenTomatoesRating
        self.file_path.props.text = media.filePath

        self.plot_buff = Gtk.TextBuffer()
        self.plot_buff.props.text = media.plot
        self.plot_box.props.buffer = self.plot_buff

        self._load_poster(media.poster)
        self.temp_poster = None

        self.media_watch_state = media.state
        self._setup_watch_state()
    
    @Gtk.Template.Callback("save")
    def save_media(self, widget):
        print("Saving the media")
        if self.temp_poster is not None:
            # We need to save the poster
            print("Updating the poster")
            update_poster_file(self.media.imdbID, self.temp_poster)
        new_media = Media(self.media.imdbID, self.title_box.props.text, self.year_box.props.text, 
                            self.rating_box.props.text, self.genre_box.props.text, self.plot_buff.props.text, 
                            self.media.poster, "", self.media.filePath, self.media.duration, 
                            self.media_watch_state, int(self.play_count.props.value))
        self.local_storage_handler.update_in_db(new_media)
        self.destroy()

    @Gtk.Template.Callback("cancel")
    def cancel_edit(self, widget):
        self.destroy()
    
    @Gtk.Template.Callback("poster_edit")
    def poster_edit(self, widget):
        file_picker = Gtk.FileChooserDialog("Select a new poster", self,
                                Gtk.FileChooserAction.OPEN,
                                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        file_picker.set_local_only(True)

        image_filter = Gtk.FileFilter()
        image_filter.set_name("Images")
        image_filter.add_pixbuf_formats()
        file_picker.add_filter(image_filter)

        response = file_picker.run()
        if response == Gtk.ResponseType.OK:
            print(f"Open clicked {file_picker.get_filename()}")

            # Copy the selected file to a temp file
            if self.temp_poster is None:
                self.temp_poster = tempfile.mkstemp()[1]
                self.connect('destroy', lambda x: os.remove(self.temp_poster))
            
            shutil.copyfile(file_picker.get_filename(), self.temp_poster)
            print(f"Temporary file saved to {self.temp_poster}")
            self._load_poster(self.temp_poster)
        
        file_picker.destroy()

    def _setup_watch_state(self):
        watch_states = Gtk.ListStore(str, str)
        selected_index = 0
        for i, state in enumerate(WatchState):
            if state == self.media_watch_state:
                selected_index = i
            watch_states.append([WatchState.make_human_readable(state), state.value])
        
        renderer_text = Gtk.CellRendererText()
        self.watch_state.props.model = watch_states
        self.watch_state.pack_start(renderer_text, True)
        self.watch_state.add_attribute(renderer_text, "text", 0)
        self.watch_state.set_active(selected_index)
        self.watch_state.connect('changed', self.watch_state_change)
    
    def watch_state_change(self, widget):
        tree_itr = widget.get_active_iter()
        if tree_itr is not None:
            model = widget.get_model()
            name, id = model[tree_itr][:2]
            print(f"Selected: ID={id}, name={name}")
            self.media_watch_state = WatchState(id)
    
    def _load_poster(self, file_path):
        self.poster_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(file_path, 300, 400)
        self.poster_image.props.pixbuf = self.poster_pixbuf
