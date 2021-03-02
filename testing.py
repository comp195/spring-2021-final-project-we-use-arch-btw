import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class MyWindow(Gtk.Window):
    def __init__(self) -> None:
        Gtk.Window.__init__(self, title="Hello World")

        self.button = Gtk.Button(label="click here")
        self.button.connect("clicked", self.on_button_click)
        self.add(self.button)

    def on_button_click(self, widget):
        print("Hello, World!")


win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
