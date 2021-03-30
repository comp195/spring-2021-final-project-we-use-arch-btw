# --- GTK Initialization ---
import os
import sys
import gi
gi.require_version("Gtk", "3.0")
gi.require_version('GdkPixbuf', '2.0')
# --- End GTK Initialization ---
from gi.repository import Gio, Gtk, GdkPixbuf
from gi.repository.GdkPixbuf import Pixbuf


@Gtk.Template(filename=os.path.join(os.path.dirname(__file__), "main.ui"))
class LVLWindow(Gtk.ApplicationWindow):
    __gtype_name__ = "LVLWindow"

    posters = Gtk.Template.Child()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.about_dialog = None
        # Icons
        temp_poster_tup = []
        path = os.path.join(os.path.dirname(__file__), "temp_posters")
        for i in os.listdir(path):
            temp_poster_tup.append((i.split(".")[0], os.path.join(path, i)))
        # print(temp_poster_tup)
        liststore = Gtk.ListStore(Pixbuf, str)
        iconview = Gtk.IconView.new()
        iconview.set_model(liststore)
        iconview.set_pixbuf_column(0)
        iconview.set_text_column(1)

        for i in temp_poster_tup:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(i[1], 50, 75)
            liststore.append([pixbuf, i[0]])
        self.posters.add(iconview)
        iconview.show()

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

    def close_about(self, *args):
        if self.about_dialog:
            self.about_dialog.hide()


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
