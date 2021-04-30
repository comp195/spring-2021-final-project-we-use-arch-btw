import appdirs
import os.path

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

app_name = "LVL"

def get_data_file(path = None):
    if path is None:
        return appdirs.user_data_dir(app_name)
    else:
        return os.path.join(appdirs.user_data_dir(app_name), path)

def get_cache_dir():
    return appdirs.user_cache_dir(app_name)


def _show_dialog(parent, message: str, type):
    dialog = Gtk.MessageDialog(parent, Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
                               type, Gtk.ButtonsType.OK, message)
    dialog.run()
    dialog.destroy()
    
def show_error_dialog(parent, message: str):
    _show_dialog(parent, message, Gtk.MessageType.ERROR)

def show_warning_dialog(parent, message: str):
    _show_dialog(parent, message, Gtk.MessageType.WARNING)

def show_info_dialog(parent, message: str):
    _show_dialog(parent, message, Gtk.MessageType.INFO)

from LVL.LocalStorageHandler.handler import LocalStorageHandler
from LVL.UI.application import Application

def run_app():
    local_storage_handler = LocalStorageHandler()
    local_storage_handler.initialize_database()
    app = Application(local_storage_handler)
    app.run()
