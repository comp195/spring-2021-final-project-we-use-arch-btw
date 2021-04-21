import appdirs
import os.path

app_name = "LVL"

def get_data_file(path = None):
    if path is None:
        return appdirs.user_data_dir(app_name)
    else:
        return os.path.join(appdirs.user_data_dir(app_name), path)

def get_cache_dir():
    return appdirs.user_cache_dir(app_name)