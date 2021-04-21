from LVL.UI.application import Application
from LVL.LocalStorageHandler.handler import LocalStorageHandler

def main():
    local_storage_handler = LocalStorageHandler()
    local_storage_handler.initialize_database()
    app = Application(local_storage_handler)
    app.run()

if __name__ == "__main__":
    main()