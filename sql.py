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

    def fetch_id(self):
        pass

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
        self.edition = self.print = None
        # slightly retarded, we first store an empty Score because we need
        # to reference the generated id in other tables at parsing
        self.cursor.execute("INSERT INTO score (genre,key,incipit,year)"
                            "VALUES (?,?,?,?)", (self.genre, self.key, self.incipit, self.year))
        self.cursor.execute("SELECT last_insert_rowid()")
        self.id = self.cursor.fetchone()[0]

    def update(self, context, data):
        setattr(self, context.split()[-1].lower(), data)

    # def fetch_id():
    # consult score_author table?

    def do_store(self):
        # here we really insert data using UPDATE
        self.cursor.execute("UPDATE score SET genre = ?, key = ?, incipit = ?, year = ?"
                            "WHERE id = ?", (self.genre, self.key, self.incipit, self.year, self.id))


class Voice(DBItem):

    def __init__(self, conn, number, data):
        super().__init__(conn)
        self.score = None  # will be updated elsewhere (this doesn't have to be here)
        self.number, self.name = number, data

    def do_store(self):
        self.cursor.execute("INSERT INTO voice (number, score, name)"
                            "VALUES (?,?,?)", (self.number, self.score, self.name))


class Edition(DBItem):

    # edition is kept (ref'd) in a Score
    def __init__(self, conn, name=None, score_id=None):
        super().__init__(conn)
        self.year = None
        self.score, self.name = score_id, name
        self.editors = []

    def do_store(self):
        self.cursor.execute("INSERT INTO edition (score, name, year)"
                            "VALUES (?,?,?)", (self.score, self.name, self.year))


class Print(DBItem):

    def __init__(self, conn, id):
        super().__init__(conn)
        self.partiture = 'N'
        self.edition = None
        self.id = id

    def do_store(self):
        self.cursor.execute("INSERT INTO print (id, partiture, edition)"
                            "VALUES (?,?,?)", (self.id, self.partiture, self.edition))


def main():
    # process a single line of input
    def process(context, data):
        if data is None or not data.strip():
            return
        data = data.strip()
        if context == 'Composer':
            for c in data.split(';'):
                p = Person(conn, c.strip())
                p.store()
                conn.execute("INSERT INTO score_author (score, composer) VALUES (?,?)", (score.id, p.id))
        elif context == 'Editor':  # side-note: there exist Editors w/out Edition(s)
            for e in data.split(','):
                p = Person(conn, e.strip())
                p.store()
                if score.edition is not None:
                    score.edition.editors.append(p)
        elif context in ['Genre', 'Key', 'Incipit', 'Composition Year']:
            score.update(context, data)
        elif context.startswith('Voice'):
            num = re.search(r"Voice ([0-9]+)", context)
            if num is not None:
                v = Voice(conn, int(num.group(1)), data)
                v.score = score.id
                v.store()
        elif context == 'Publication Year':
            if score.edition is None:
                score.edition = Edition(conn, score_id=score.id)
            non_digit_pos = re.search(r"\D", data)
            if non_digit_pos:
                data = data[0:non_digit_pos.start()]
            score.edition.year = int(data)
        elif context == 'Edition':
            if score.edition is None:
                score.edition = Edition(conn, data, score.id)
            else:
                score.edition.name = data
        elif context == 'Print Number':
            score.print = Print(conn, int(data))
        elif context == 'Partiture':
            if data.startswith('yes'):
                score.print.partiture = 'P' if re.search(r"partial", data) is not None else 'Y'

    conn = sqlite3.connect('scorelib.dat')
    for table in ['person', 'score', 'score_author', 'voice', 'edition', 'edition_author', 'print']:
        conn.cursor().execute("DELETE FROM %s" % table)  # erase tables

    f = open('scorelib.txt', 'r')
    r = re.compile(r"(.*):(.*)")  # compile pattern out of loop
    score = Score(conn)

    for line in f:
        if not line.strip():  # line empty
            if score.print is None:  # multiple blank lines (TODO deal w/ better)
                continue
            score.do_store()
            if score.edition is not None:
                score.edition.store()
                for e in score.edition.editors:
                    conn.execute("INSERT INTO edition_author (edition, editor)"
                                 "VALUES (?,?)", (score.edition.id, e.id))
                score.print.edition = score.edition.id
                score.print.do_store()
            score = Score(conn)  # empty Score created & inserted (generated id)
        m = r.match(line)
        if m is not None:
            process(m.group(1), m.group(2))

    conn.commit()

if __name__ == '__main__':
    main()
