# pylint: disable=no-member
from LVL.Media.media import Media
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import os

@Gtk.Template(filename=os.path.join(os.path.dirname(__file__), "bulk_import_dialog.ui"))
class BulkImport(Gtk.Window):

    __gtype_name__ = "BulkImportDialog"

    entry_list = Gtk.Template.Child()

    def __init__(self, autodetected_media) -> None:
        super().__init__()
        
        self.built_entries = {}
        self.autodetected_media = autodetected_media
        self.populate_entries()


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
        builder.add_from_file(os.path.join(os.path.dirname(__file__), "bulk_import_entry.ui"))

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
    
    def on_edit(self, _widget, media):
        print(f"Editing media {media}")
