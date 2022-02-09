import os
import sqlite3
from functools import cached_property

from .setup import delete_database, setup_database, fill_database


class Database:
    def __init__(self, db_string="example.db"):
        if not os.path.exists(db_string):
            Database.setup(db_string)

        self.con = sqlite3.connect(db_string)
        self.cur = self.con.cursor()

    def run(self, cmd):
        print(cmd)
        results = self.cur.execute(cmd).fetchall()
        print(results)
        return results

    @cached_property
    def get_units(self):
        return self.run("SELECT * FROM unit;")

    @cached_property
    def get_unittypes(self):
        return self.run("SELECT * FROM unittype;")

    @cached_property
    def get_si_units(self):
        return self.run("SELECT rowid FROM unit WHERE conversion = 1.0;")

    def to_unitid(self, unit):
        if not unit:
            return None

        result = self.run(
            f"""
            SELECT rowid, unittypeid FROM unit WHERE shortname = '{unit}';
        """
        )

        return result[0] if result else None

    def to_categoryid(self, category):
        if not category:
            return None

        result = self.run(
            f"""
            SELECT rowid FROM category WHERE name = '{category}';
        """
        )

        return result[0][0] if result else None

    # @lru_cache
    def get_conversion_factor(self, unitid):
        result = self.run(
            f"""
            SELECT conversion FROM unit WHERE rowid = {unitid};
        """
        )

        return result[0][0] if result else None

    def look_up(self, min_value, max_value=None, unittypeid=None, categoryid=None):
        # TODO clean sql queries

        # TODO support categories

        # TODO Also search through "understandable" units, all converted
        # should be possible with a neat sql query

        if unittypeid:
            unit_filter = f"AND unittypeid = {unittypeid}"
        else:
            unit_filter = ""

        if max_value is not None:
            value_filter = f"value BETWEEN {min_value} AND {max_value}"
        else:
            value_filter = f"value = {min_value}"

        results = self.run(
            f"""
            SELECT * FROM number_computed WHERE {value_filter} {unit_filter};
        """
        )

        return results

    @staticmethod
    def setup(db_string):
        delete_database(db_string)
        setup_database(db_string)
        fill_database(db_string)
