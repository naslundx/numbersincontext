import json
import os
from flask import Flask, render_template, request
from backend import Database, search


app = Flask(__name__, static_folder="build/static", template_folder="build")
Database()


@app.get("/api/lookup")
def lookup():
    value = request.args.get("value", type=float)
    if not value or value < 0:
        return "", 400

    unit = request.args.get("unit", type=str) or "none"
    category = request.args.get("category", default=None, type=str)

    db = Database()
    unit_data, categoryid = db.to_unitid(unit), db.to_categoryid(category)

    if not unit_data:
        return "", 400

    unitid, unittypeid = unit_data
    result = search(value, unitid, unittypeid, categoryid)
    return json.dumps(result)


@app.get("/api/units")
def get_units():
    db = Database()
    return json.dumps(
        [
            {"id": row[0], "shortname": row[1], "name": row[2], "type": row[3]}
            for row in db.get_units
        ]
    )


@app.get("/api/unittypes")
def get_unittypes():
    db = Database()
    return json.dumps([{"id": row[0], "name": row[1]} for row in db.get_unittypes])


@app.get("/")
def hello():
    return render_template("index.html")


print("Starting Flask!")

app.debug = True
app.run(host="0.0.0.0", port=os.environ.get("PORT", "5000"))
