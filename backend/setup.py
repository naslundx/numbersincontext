import sqlite3

def _run(db_string, cmd):
    con = sqlite3.connect(db_string)
    cur = con.cursor()
    cur.execute(cmd)
    con.commit()
    cur.close()


def _get(db_string, cmd):
    con = sqlite3.connect(db_string)
    cur = con.cursor()
    result = cur.execute(cmd)
    return result


def delete_database(db_string = "example.db"):
    _run(db_string, "DROP TABLE IF EXISTS unit")
    _run(db_string, "DROP TABLE IF EXISTS unittype")
    _run(db_string, "DROP TABLE IF EXISTS category")
    _run(db_string, "DROP TABLE IF EXISTS number")
    _run(db_string, "DROP TABLE IF EXISTS numbercategories")


def setup_database(db_string = "example.db"):
    _run(db_string, """
        CREATE TABLE unittype(
            rowid INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE
        );
    """)

    _run(db_string, """
        CREATE TABLE unit(
            rowid INTEGER PRIMARY KEY,
            shortname TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL UNIQUE,
            unittypeid INTEGER,
            conversion REAL NOT NULL,
            FOREIGN KEY (unittypeid) REFERENCES unittype(rowid)
        );
    """)

    _run(db_string, """
        CREATE TABLE category(
            rowid INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            description TEXT
        );
    """)

    _run(db_string, """
        CREATE TABLE number(
            rowid INTEGER PRIMARY KEY,
            value INTEGER NOT NULL,
            unittypeid INTEGER NOT NULL,
            description TEXT NOT NULL,
            FOREIGN KEY (unittypeid) REFERENCES unittype(rowid),
            UNIQUE (value, unittypeid)
        );
    """)

    _run(db_string, """
        CREATE TABLE numbercategories(
            categoryid INTEGER NOT NULL,
            numberid INTEGER NOT NULL,
            FOREIGN KEY (categoryid) REFERENCES category(rowid),
            FOREIGN KEY (numberid) REFERENCES number(rowid),
            UNIQUE (categoryid, numberid)
        );
    """)


def fill_database(db_string = "example.db"):
    _run(db_string, """
        INSERT INTO unittype(name)
        VALUES ('none'), ('distance'), ('time');
    """)

    _run(db_string, """
        INSERT INTO unit(shortname, name, unittypeid, conversion)
        VALUES 
            ('n/a', 'none', 1, 1),

            ('km', 'kilometer', 2, 1000),
            ('m', 'meter', 2, 1),
            ('dm', 'decimeter', 2, 0.1),
            ('cm', 'centimeter', 2, 0.01),
            ('mm', 'millimeter', 2, 0.001),
            
            ('ms', 'millisecond', 3, 0.001),
            ('s', 'second', 3, 1),
            ('min', 'minute', 3, 60),
            ('hr', 'hour', 3, 3600),
            ('day', 'day', 3, 86400),
            ('yr', 'year', 3, 31536000);
    """)

    _run(db_string, """
        INSERT INTO number(value, unittypeid, description)
        VALUES 
            (1, 1, 'A single item'),
            (11, 1, 'Number of players in a football team'),
            (100, 1, 'Temperature at which water boils'),
            (1000, 1, 'Distance 1 KM apart');
    """)
