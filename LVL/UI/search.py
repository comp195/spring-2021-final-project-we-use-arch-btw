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
from LVL.LocalStorageHandler.poster_handler import get_poster_file, download_poster
from LVL.LocalStorageHandler.handler import LocalStorageHandler
from LVL.LocalStorageHandler.media_title_parser import parse_file
from LVL.omdbapi import omdb_search, omdb_get, parse_result, search_by_title


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

    def __init__(self, title, media_file, application, handler: LocalStorageHandler):
        super().__init__(application=application)
        
        self.media_file = media_file
        self.search_title = title
        self.search.props.text = title
        self.local_storage_handler = handler
        
        self.update_results()

    def update_results(self):
        self.search_title = self.search.props.text
        results = search_by_title(self.search_title)

        current_rows = self.lists.get_children()
        for i in current_rows:
            self.lists.remove(i)

        if results is not None:
            for i in results:
                row = ListBoxRowWithData(i[0], i[1])
                self.lists.add(row)
                row.show_all()

    
    @Gtk.Template.Callback("save")
    def save_media(self, widget):
        print("Saving the media")
        selected_id = self.lists.get_selected_row().imdbID
        omdb_data = omdb_get(selected_id)
        new_media_obj = parse_result(omdb_data)
        new_media_obj.filePath = self.media_file
        self.local_storage_handler.save_media_to_db(new_media_obj)
        download_poster(new_media_obj.imdbID)
        self.destroy()

    @Gtk.Template.Callback("cancel")
    def cancel_edit(self, widget):
        self.destroy()

    @Gtk.Template.Callback("clicked_find")
    def clicked_find(self, widget):
        self.update_results()
    
    def do_key_press_event(self, event):
        if event.keyval == Gdk.KEY_Return:
            self.update_results()
        return Gtk.ApplicationWindow.do_key_press_event(self, event)
