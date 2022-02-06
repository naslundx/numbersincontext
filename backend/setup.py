import sqlite3

def _run(cmd, db_string = "example.db"):
    con = sqlite3.connect(db_string)
    cur = con.cursor()
    cur.execute(cmd)
    con.commit()
    cur.close()


def _get(cmd, db_string = "example.db"):
    con = sqlite3.connect(db_string)
    cur = con.cursor()
    result = cur.execute(cmd)
    return result


def delete_database(db_string = "example.db"):
    _run("DROP TABLE IF EXISTS unit")
    _run("DROP TABLE IF EXISTS unittype")
    _run("DROP TABLE IF EXISTS category")
    _run("DROP TABLE IF EXISTS number")
    _run("DROP TABLE IF EXISTS numbercategories")


def setup_database(db_string = "example.db"):
    _run("""
        CREATE TABLE unittype(
            rowid INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE
        )
    """)

    _run("""
        CREATE TABLE unit(
            rowid INTEGER PRIMARY KEY,
            shortname TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL UNIQUE,
            type INTEGER,
            conversion REAL NOT NULL,
            FOREIGN KEY (type) REFERENCES unittype(rowid)
        )
    """)

    _run("""
        CREATE TABLE category(
            rowid INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE
        )
    """)

    _run("""
        CREATE TABLE number(
            rowid INTEGER PRIMARY KEY,
            value INTEGER NOT NULL,
            unitid INTEGER NOT NULL,
            description TEXT NOT NULL,
            FOREIGN KEY (unitid) REFERENCES unittype(rowid),
            UNIQUE (value, unitid)
        )
    """)

    _run("""
        CREATE TABLE numbercategories(
            categoryid INTEGER NOT NULL,
            numberid INTEGER NOT NULL,
            FOREIGN KEY (categoryid) REFERENCES category(rowid),
            FOREIGN KEY (numberid) REFERENCES number(rowid),
            UNIQUE (categoryid, numberid)
        )
    """)


def fill_database(db_string = "example.db"):
    _run("""
        INSERT INTO unittype(name)
        VALUES ('distance'), ('time');
    """)

    _run("""
        INSERT INTO unit(shortname, name, type, conversion)
        VALUES 
            ('m', 'meter', 1, 1),
            ('dm', 'decimeter', 1, 10),
            
            ('s', 'second', 2, 1),
            ('min', 'minute', 2, 1.0/60);
    """)

    _run("""
        INSERT INTO number(value, unitid, description)
        VALUES 
            (1, 1, 'A single item'),
            (11, 1, 'Number of players in a football team'),
            (100, 1, 'Temperature at which water boils'),
            (1000, 1, 'Distance 1 KM apart');
    """)


delete_database()
setup_database()
fill_database()

# for row in _get('SELECT * FROM number;'):
#     print(row)