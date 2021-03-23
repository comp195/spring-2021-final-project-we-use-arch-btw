# --- GTK Initialization ---
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gio, Gtk
# --- End GTK Initialization ---
import sys
import os


@Gtk.Template(filename = os.path.join(os.path.dirname(__file__), "main.ui"))
class LVLWindow(Gtk.ApplicationWindow):
    __gtype_name__ = "LVLWindow"


    @Gtk.Template.Callback("button_click")
    def on_button_click(self, *args):
        print(f"Button was clicked with {args}")


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
