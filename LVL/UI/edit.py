# pylint: disable=no-member
from LVL.Media.media import Media
from LVL.Media.state import State as WatchState
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
    plot_box = Gtk.Template.Child()
    poster_image = Gtk.Template.Child()
    watch_state = Gtk.Template.Child()
    play_count = Gtk.Template.Child()

    def __init__(self, media: Media, application):
        super().__init__(application=application)

        self.media = media

        self.title_box.props.text = media.title
        self.year_box.props.text = media.year
        self.genre_box.props.text = media.genre
        self.rating_box.props.text = media.rating
        self.play_count.props.value = media.playCount

        self.plot_buff = Gtk.TextBuffer()
        self.plot_buff.props.text = media.plot
        self.plot_box.props.buffer = self.plot_buff

        self.poster_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(media.poster, 300, 400)
        self.poster_image.props.pixbuf = self.poster_pixbuf

        self.media_watch_state = media.state
        self._setup_watch_state()
    
    @Gtk.Template.Callback("save")
    def save_media(self, widget):
        print("Saving the media")
        pass

    @Gtk.Template.Callback("cancel")
    def cancel_edit(self, widget):
        self.destroy()

    def _setup_watch_state(self):
        watch_states = Gtk.ListStore(str, str)
        state_lookup = {
            WatchState.IN_PROGRESS: 'In Progress',
            WatchState.UNWATCHED: 'Unwatched',
            WatchState.WATCHED: 'Watched'
        }
        selected_index = 0
        for i, state in enumerate(WatchState):
            if state == self.media_watch_state:
                selected_index = i
            watch_states.append([state_lookup[state], state.value])
        
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
