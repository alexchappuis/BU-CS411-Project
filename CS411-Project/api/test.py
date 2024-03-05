import sqlite3


class ExampleObject:
    def __init__(self, name="", favGame=""):
        self.id = -1
        self.name = name
        self.favGame = favGame
        self.connection = sqlite3.connect("test.db")
        self.cursor = self.connection.cursor()

    def load_season(self, id: int):
        """
        Load a user from the database using the provided ID.

        Parameters
        ----------
        id: int
            ID of the user to load

        Returns
        -------
        bool
            Whether or not a user with the provided ID exists and was loaded
        """

        self.cursor.execute(
            """
        SELECT * FROM users
        WHERE id = ?
        """,
            (id,),
        )

        row = self.cursor.fetchone()
        if row is None:
            return False

        self.id = row[0]
        self.name = row[1]
        self.favGame = row[2]
        return True

    def insert_user(self):
        """
        Insert this user into the database.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        self.cursor.execute(
            """
        INSERT INTO users
        (name, favGame)
        VALUES
        (?, ?)
        """,
            (self.name, self.favGame),
        )
        self.connection.commit()

    def toJSON(self):
        """
        Create a JSON object for this user's data.

        Parameters
        ----------
        None

        Returns
        -------
        dict
            JSON object representation of this user's data.
        """

        return {
            "id": self.id,
            "name": self.name,
            "favGame": self.favGame,
        }

    @staticmethod
    def makeExampleTable():
        """
        Create the example table in test.db if it doesn't yet exist.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        connection = sqlite3.connect("test.db")
        cursor = connection.cursor()
        sql = """CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            favGame TEXT NOT NULL
        );"""
        cursor.execute(sql)
        connection.commit()
        connection.close()
