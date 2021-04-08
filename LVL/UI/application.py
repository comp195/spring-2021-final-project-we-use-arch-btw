# pylint: disable=no-member
# --- GTK Initialization ---
import os
import sys
import gi
gi.require_version("Gtk", "3.0")
gi.require_version('GdkPixbuf', '2.0')
# --- End GTK Initialization ---
from gi.repository import Gio, Gtk, GdkPixbuf, Gdk

from fuzzywuzzy import process


@Gtk.Template(filename=os.path.join(os.path.dirname(__file__), "main.ui"))
class LVLWindow(Gtk.ApplicationWindow):
    __gtype_name__ = "LVLWindow"

    posters = Gtk.Template.Child()
    search_entry = Gtk.Template.Child()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.about_dialog = None
        self.poster_list = {}
        self.poster_gobjects = {}
        self.search_query = ""

        # This is temporary
        path = os.path.join(os.path.dirname(__file__), "temp_posters")
        for i in os.listdir(path):
            self.poster_list[os.path.splitext(i)[0]] =  os.path.join(path, i)
            self.poster_gobjects[os.path.join(path, i)] = GdkPixbuf.Pixbuf.new_from_file_at_size(os.path.join(path, i), 50, 75)

        self.liststore = Gtk.ListStore(GdkPixbuf.Pixbuf, str)
        iconview = Gtk.IconView.new()
        iconview.set_model(self.liststore)
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
            self.liststore.clear()
            ranked = process.extract(self.search_query, self.poster_list.keys())
            for entry, score in ranked:
                if score < 50:
                    continue
                self.liststore.append([self.poster_gobjects[self.poster_list[entry]], entry])
        else:
            # Show everything on an empty search
            self.liststore.clear()
            for name, path in self.poster_list.items():
                self.liststore.append([self.poster_gobjects[path], name])
        pass

    def close_about(self, *args):
        if self.about_dialog:
            self.about_dialog.hide()
    
    def on_media_select(self, iconview):
        selected = iconview.get_selected_items()
        if len(selected) > 0:
            index = selected[0].get_indices()[0] # This will probably break at some point but yolo
            print(f"Selected item {index}, we should probably open a dialog here or something")
            iconview.unselect_all()


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
