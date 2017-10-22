import json
import sqlite3
import sys

conn = sqlite3.connect('scorelib_o.dat')
# IN: composer name (substring),
# OUT: all matching composers, all their scores in the database (optionally w/ print #s)

# map composer => list of scores (as maps themselves)
composers = {}


def add_to_map(tupl):
    name, score, title, key, v_no, v_name = tupl  # unpack tuple
    ret = {
        "score": score,
        "title": title,
        "key": key
    }

    if name not in composers:
        if v_no or v_name:
            ret["voices"] = {v_no: v_name}
        composers[name] = []
    for sc in composers[name]:
        if score == sc['score']:
            if v_no or v_name:
                if "voices" not in sc:
                    sc["voices"] = {v_no: v_name}
                else:
                    sc["voices"][v_no] = v_name
            return
    composers[name].append(ret)


for item in conn.execute("SELECT person.name,score_author.score,score.name,key,"
                         "voice.number,voice.name FROM "
                         "person JOIN score_author ON person.id = composer "
                         "JOIN score ON score_author.score = score.id "
                         "LEFT JOIN voice ON score_author.score = voice.score "
                         "WHERE person.name LIKE \"%" + sys.argv[1] + "%\""):
    add_to_map(item)

json.dump(composers, sys.stdout, indent=4)
