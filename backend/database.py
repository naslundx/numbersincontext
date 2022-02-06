import sqlite3
from functools import cached_property

from .setup import *


class Database:
    def __init__(self, db_string = "example.db"):
        self.con = sqlite3.connect(db_string)
        self.cur = self.con.cursor()


    @cached_property
    def get_units(self):
        results = self.cur.execute("""
            SELECT * FROM unit;
        """).fetchall()
        return results


    @cached_property
    def get_unittypes(self):
        results = self.cur.execute("""
            SELECT * FROM unittype;
        """).fetchall()
        return results


    def look_up(self, value, unit=None, category=None, tolerance=0):
        # TODO assert we're doing this with proper unittype (SI unit)

        # TODO clean sql queries

        # TODO support categories

        if unit:
            unit_filter = f" AND unitid = {unit}"
        else:
            unit_filter = ""
            
        if tolerance:
            low, high = value * (1 - tolerance), value * (1 + tolerance)
            value_filter = f"value BETWEEN {low} AND {high}"
        else:
            value_filter = f"value = {value}"

        results = self.cur.execute(f"""
            SELECT * FROM number WHERE {value_filter} {unit_filter};
        """).fetchall()

        return results

    @staticmethod
    def setup():
        delete_database()
        setup_database()
        fill_database()
