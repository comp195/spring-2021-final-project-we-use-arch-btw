from LVL.UI.application import Application
from LVL.LocalStorageHandler.handler import LocalStorageHandler

def main():
    local_storage_handler = LocalStorageHandler()
    local_storage_handler.initialize_database()
    app = Application(local_storage_handler)
    app.run()

if __name__ == "__main__":
    main()

    # Test data, put in after initialize_database()
    # p1 = "After the devastating events of Avengers: Infinity War (2018), the universe is in ruins. With the help of remaining allies, the Avengers assemble once more in order to reverse Thanos' actions and restore balance to the universe."
    # local_storage_handler.save_to_db("tt4154796", "Avengers: Endgame", "2019", "PG-13", "Action, Adventure, Drama, Sci-Fi",
    # p1, "94%", "/home/user/Desktop/avengers.mp4", "181 min", "WATCHED", 2)
    # p2 = "Johnny is a successful bank executive who lives quietly in a San Francisco townhouse with his fiancée, Lisa. One day, putting aside any scruple, she seduces Johnny's best friend, Mark. From there, nothing will be the same again."
    # local_storage_handler.save_to_db("tt0368226", "The Room", "2003", "R", "Drama", p2, "24%", "/home/user/Desktop/theroom.mp4", "99 min", "UNWATCHED", 0)
    # p3 = "As Harvard student Mark Zuckerberg creates the social networking site that would become known as Facebook, he is sued by the twins who claimed he stole their idea, and by the co-founder who was later squeezed out of the business."
    # local_storage_handler.save_to_db("tt1285016", "The Social Network", "2010", "PG-13", "Biography, Drama", p3, "96%", "/home/user/Desktop/thesocialnetwork.mp4", "120 min", "WATCHED", 1)
