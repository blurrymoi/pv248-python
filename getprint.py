import json
import sqlite3
import sys

# json.dumps (=dump to string)
# keys are always strings in json >>

'''
d = {}
d["composer"]=["Bach, Johann Sebastian"]
d["key"]="g"
d["voices"]=
{ 1 : "oboe",
2 : "bassoon" }
json.dump(d,sys.stdout,indent=4)
'''

conn = sqlite3.connect('scorelib_o.dat')
# sys.argv[1]
# IN: print number, OUT: list of composers
# the result of cursor.execute is iterable !

'''
scores = conn.execute("SELECT score FROM print JOIN edition ON print.edition = edition.id "
                        "WHERE print.id=?", (sys.argv[1],))
names = []
for (score,) in scores:
    authors = conn.execute("SELECT composer FROM score_author WHERE score=?", (score,))

    for (auth_id,) in authors:
        names.append(conn.execute("SELECT name FROM person WHERE id=?", (auth_id,)).fetchone())

for (c,) in names:
    print(c)
'''

# mushed #o_p# #

names = conn.execute("SELECT person.name FROM person WHERE person.id IN "
                     "(SELECT composer FROM score_author WHERE score IN "
                     "(SELECT score FROM print JOIN edition ON print.edition = edition.id WHERE print.id=?))", (sys.argv[1],))

for (c,) in names:
    print(c)
