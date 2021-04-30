# pylint: disable=no-member
from LVL.UI import MediaGObject
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GObject
import os
from LVL.omdbapi import omdb_get, parse_result, search_by_title

class ListBoxRowWithData(Gtk.ListBoxRow):
    def __init__(self, title, imdbID, year):
        super().__init__()
        self.title = title
        self.year = year
        self.imdbID = imdbID
        self.add(Gtk.Label(label=f"{self.title} ({self.year})"))

@Gtk.Template(filename=os.path.join(os.path.dirname(__file__), "search.ui"))
class SearchWindow(Gtk.Window):
    
    __gtype_name__ = "SearchWindow"

    __gsignals__ = {
        "media-selected": (GObject.SIGNAL_RUN_FIRST, None, (MediaGObject,))
    }

    search = Gtk.Template.Child()
    lists = Gtk.Template.Child()

    def __init__(self, title, media_file):
        super().__init__()
        
        self.media_file = media_file
        self.search_title = title
        self.search.props.text = title
        
        self.update_results()

    def update_results(self):
        self.search_title = self.search.props.text
        results = search_by_title(self.search_title)

        current_rows = self.lists.get_children()
        for i in current_rows:
            self.lists.remove(i)

        if results is not None:
            for i in results:
                row = ListBoxRowWithData(i[0], i[1], i[2])
                self.lists.add(row)
                row.show_all()

    
    @Gtk.Template.Callback("save")
    def save_media(self, widget):
        print("Saving the media")
        selected_id = self.lists.get_selected_row().imdbID
        omdb_data = omdb_get(selected_id)
        new_media_obj = parse_result(omdb_data)
        new_media_obj.filePath = self.media_file
        self.emit('media-selected', MediaGObject(new_media_obj))

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
