import re
import sqlite3


class DBItem:
    """
    This is a base class for objects that represent database items. It implements
    the store() method in terms of fetch_id and do_store, which need to be
    implemented in every derived class (see Person below for an example).
    """
    def __init__(self, conn):
        self.id = None
        self.cursor = conn.cursor()

    def store(self):
        self.fetch_id()
        if self.id is None:
            self.do_store()
            self.cursor.execute("SELECT last_insert_rowid()")
            self.id = self.cursor.fetchone()[0]


class Person(DBItem):
    """
    Example of a class which represents a single row of a single database table.
    This is a very simple example, since it does not contain any references to
    other objects.
    """
    def __init__(self, conn, string):
        super().__init__(conn)
        self.name = re.sub('\([0-9+-]+\)', '', string).strip()
        m = re.search('\(([0-9]+)-+([0-9]*)\)', string)
        if m is not None:
            self.born = int(m.group(1))
            self.died = int(m.group(2)) if m.group(2) else None
        else:
            self.born = self.died = None

    def fetch_id(self):
        self.cursor.execute("SELECT id,born,died FROM person WHERE name = ?", (self.name,))
        res = self.cursor.fetchone()
        if res is not None:
            self.id = res[0]
            if self.born is not None and res[1] is None:
                self.cursor.execute("UPDATE person SET born = ? WHERE id = ?", (self.born, self.id))
            if self.died is not None and res[2] is None:
                self.cursor.execute("UPDATE person SET died = ? WHERE id = ?", (self.died, self.id))

    def do_store(self):
        self.cursor.execute("INSERT INTO person (name,born,died) VALUES (?,?,?)", (self.name, self.born, self.died))


class Score(DBItem):

    def __init__(self, conn):
        super().__init__(conn)
        self.genre = self.key = self.incipit = self.year = None

    def update(self, context, data):
        setattr(self, context.split()[-1].lower(), data)

    def fetch_id(self):
        return None
        # consult score_author table?

    def do_store(self):
        self.cursor.execute("INSERT INTO score (genre,key,incipit,year)"
                            "VALUES (?,?,?,?)", (self.genre, self.key, self.incipit, self.year))


def main():
    # process a single line of input
    def process(context, data):
        if data is None:
            pass
        if context == 'Composer':
            for c in data.split(';'):
                p = Person(conn, c.strip())
                p.store()
        elif context in ['Genre', 'Key', 'Incipit', 'Composition Year']:
            score.update(context, data)

    conn = sqlite3.connect('scorelib.dat')
    # conn.cursor().execute("DELETE FROM person")

    f = open('scorelib.txt', 'r')
    r = re.compile(r"(.*):(.*)")  # compile pattern out of loop
    score = Score(conn)

    for line in f:
        if not line.strip():  # line empty
            score.store()
            score = Score(conn)
        m = r.match(line)
        if m is None:
            continue
        process(m.group(1), m.group(2))

    conn.commit()

if __name__ == '__main__':
    main()
