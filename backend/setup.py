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


def delete_database(db_string="example.db"):
    _run(db_string, "DROP TABLE IF EXISTS unit")
    _run(db_string, "DROP TABLE IF EXISTS unittype")
    _run(db_string, "DROP TABLE IF EXISTS category")
    _run(db_string, "DROP TABLE IF EXISTS number")
    _run(db_string, "DROP TABLE IF EXISTS numbercategories")


def setup_database(db_string="example.db"):
    _run(
        db_string,
        """
        CREATE TABLE unittype(
            rowid INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE
        );
    """,
    )

    _run(
        db_string,
        """
        CREATE TABLE unit(
            rowid INTEGER PRIMARY KEY,
            shortname TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL UNIQUE,
            unittypeid INTEGER,
            conversion REAL NOT NULL,
            FOREIGN KEY (unittypeid) REFERENCES unittype(rowid)
        );
    """,
    )

    _run(
        db_string,
        """
        CREATE TABLE category(
            rowid INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            description TEXT
        );
    """,
    )

    _run(
        db_string,
        """
        CREATE TABLE number(
            rowid INTEGER PRIMARY KEY,
            value INTEGER NOT NULL,
            unittypeid INTEGER NOT NULL,
            description TEXT NOT NULL,
            FOREIGN KEY (unittypeid) REFERENCES unittype(rowid),
            UNIQUE (value, unittypeid)
        );
    """,
    )

    _run(
        db_string,
        """
        CREATE TABLE numbercategories(
            categoryid INTEGER NOT NULL,
            numberid INTEGER NOT NULL,
            FOREIGN KEY (categoryid) REFERENCES category(rowid),
            FOREIGN KEY (numberid) REFERENCES number(rowid),
            UNIQUE (categoryid, numberid)
        );
    """,
    )


def fill_database(db_string="example.db"):
    _run(
        db_string,
        """
        INSERT INTO unittype(name)
        VALUES 
            ('none'), 
            ('distance'), 
            ('time'), 
            ('temperature');
    """,
    )

    _run(
        db_string,
        """
        INSERT INTO unit(shortname, name, unittypeid, conversion)
        VALUES 
            ('none', 'none', 1, 1),

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
            ('yr', 'year', 3, 31536000),

            ('c', 'celsius', 4, 1);
    """,
    )

    _run(
        db_string,
        """
        INSERT INTO number(value, unittypeid, description)
        VALUES 
            (11, 1, 'Number of players in a football team'),
            (100, 1, 'Temperature (C) at which water boils'),
            (1605430, 1, 'Population of Stockholm'),
            (583056, 1, 'Population of Göteborg'),
            (1412600000, 1, 'Population of China'),
            (333186076, 1, 'Population of USA'),
            (125440000, 1, 'Population of Japan'),
            (67081234, 1, 'Population of UK'),
            (10449381, 1, 'Population of Sweden'),
            (888005, 1, 'Population of Cyprus'),
            (53686, 1, 'Population of Faroe Islands'),
            (825, 1, 'Population of Vatican City'),
            (32, 1, 'Number of pieces on a chessboard'),
            (11700, 1, 'Years since last ice age'),
            (233, 1, 'Years since the French revolution'),

            (1.77, 2, 'Average length of a human'),
            (4.6, 2, 'Average length of a car'),
            (381, 2, 'Height of Empire State Building'),
            (64000, 2, 'Distance between Stockholm and Uppsala'),
            (397000, 2, 'Distance between Stockholm and Göteborg'),
            
            (60*3, 3, 'Time of a Eurovision contest song');
    """,
    )

    _run(
        db_string,
        """
        CREATE TABLE number_computed AS
            SELECT 
                n.description AS description, 
                n.value / u.conversion AS value, 
                n.unittypeid AS unittypeid,
                u.shortname AS unitshortname,
                u.rowid AS unitid
            FROM 
                number AS n, 
                unit AS u 
            WHERE 
                n.unittypeid = u.unittypeid;
    """,
    )
