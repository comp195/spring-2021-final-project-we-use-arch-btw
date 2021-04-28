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
from LVL.API.handler import search_by_title


class ListBoxRowWithData(Gtk.ListBoxRow):
    def __init__(self, title, imdbID):
        super().__init__()
        self.title = title
        self.imdbID = imdbID
        self.add(Gtk.Label(label=title))

@Gtk.Template(filename=os.path.join(os.path.dirname(__file__), "search.ui"))
class SearchWindow(Gtk.Window):
    
    __gtype_name__ = "SearchWindow"

    search = Gtk.Template.Child()
    lists = Gtk.Template.Child()

    def __init__(self, title, application, handler: LocalStorageHandler):
        super().__init__(application=application)
        
        self.search_title = title
        self.search.props.text = title
        self.local_storage_handler = handler
        
        self.update_results()

    def update_results(self):
        results = search_by_title("Star Wars")
        if results is not None:
            for i in results:
                row = ListBoxRowWithData(i[0], i[1])
                self.lists.add(row)
                row.show_all()

    
    @Gtk.Template.Callback("save")
    def save_media(self, widget):
        print("Saving the media")
        # if self.temp_poster is not None:
        #     # We need to save the poster
        #     print("Updating the poster")
        #     update_poster_file(self.media.imdbID, self.temp_poster)
        # new_media = Media(self.media.imdbID, self.title_box.props.text, self.year_box.props.text, 
        #                     self.rating_box.props.text, self.genre_box.props.text, self.plot_buff.props.text,
        #                     self.rotten_tomatoes.props.text, self.media.filePath, self.media.duration, 
        #                     self.media_watch_state, int(self.play_count.props.value))
        # self.local_storage_handler.update_in_db(new_media)
        self.destroy()

    @Gtk.Template.Callback("cancel")
    def cancel_edit(self, widget):
        self.destroy()

    @Gtk.Template.Callback("search_change")
    def search_change(self, widget):
        self.search_title = widget.props.text

    # def do_key_press_event(self, event):
    #     print(event.keyval)
    #     if event.keyval == Gdk.KEY_Enter:
    #         print("Hit Enter")
    #     return Gtk.ApplicationWindow.do_key_press_event(self, event)
