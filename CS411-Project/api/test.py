import sqlite3


class ExampleObject:
    def __init__(self, name, favGame):
        self.name = name
        self.favGame = favGame
        self.connection = sqlite3.connect("test.db")
        self.cursor = self.connection.cursor()

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
        INSERT INTO example
        (name, favGame)
        VALUES
        (?, ?)
        """,
            (self.name, self.favGame),
        )
        self.connection.commit()

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
        sql = """CREATE TABLE IF NOT EXISTS example (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            favGame TEXT NOT NULL
        );"""
        cursor.execute(sql)
        connection.commit()
        connection.close()
