import os
import sqlite3
from functools import cached_property

from .setup import *


class Database:
    def __init__(self, db_string = "example.db"):
        if not os.path.exists(db_string):
            Database.setup(db_string)

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


    @cached_property
    def get_si_units(self):
        results = self.cur.execute("""
            SELECT rowid FROM unit WHERE conversion = 1.0;
        """).fetchall()
        return results


    def to_unitid(self, unit):
        if not unit:
            return None

        result = self.cur.execute(f"""
            SELECT rowid, unittypeid FROM unit WHERE shortname = '{unit}';
        """).fetchone()
        return result


    def to_categoryid(self, category):
        if not category:
            return None

        result = self.cur.execute(f"""
            SELECT rowid FROM category WHERE name = '{category}';
        """).fetchone()
        return result[0]


    # @lru_cache
    def get_conversion_factor(self, unitid):
        result = self.cur.execute(f"""
            SELECT conversion FROM unit WHERE rowid = {unitid};
        """).fetchone()
        return result[0]

    def look_up(self, value, unittypeid=None, categoryid=None, tolerance=0):
        # TODO clean sql queries

        # TODO support categories

        if unittypeid:
            unit_filter = f"AND unittypeid = {unittypeid}"
        else:
            unit_filter = ""
            
        if tolerance:
            low, high = value * (1 - tolerance), value * (1 + tolerance)
            value_filter = f"value BETWEEN {low} AND {high}"
        else:
            value_filter = f"value = {value}"

        print(f"SELECT * FROM number WHERE {value_filter} {unit_filter};")

        results = self.cur.execute(f"""
            SELECT * FROM number WHERE {value_filter} {unit_filter};
        """).fetchall()

        print(results)

        return results

    @staticmethod
    def setup(db_string):
        delete_database(db_string)
        setup_database(db_string)
        fill_database(db_string)
