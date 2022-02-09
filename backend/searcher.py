import math
from .database import Database


def remove_doubles(data):
    idx = 0
    while idx < len(data):
        found = False
        for jdx in range(idx + 1, len(data)):
            e, e2 = data[idx], data[jdx]
            if e["value"] == e2["value"] and e["unit"] == e2["unit"] and e["score"] < e2["score"]:
                data.pop(jdx)
                found = True
                break
        if not found:
            idx += 1


def search(original_value: int, unitid: int, unittypeid: int, categoryid: int):
    if not unitid:
        return []

    # === SETUP ===

    # Setup database
    db = Database()

    # Convert to proper SI unit
    # if unitid not in db.get_si_units:
    #     factor = db.get_conversion_factor(unitid)
    #     value = original_value * factor
    # else:
    value = original_value

    # === EXACT MATCHES ===

    # Look for exact match
    results_exact = db.look_up(value)

    # === APPROXIMATE MATCHES (10%) ===

    # Approximate near
    tolerance = 0.101
    low, high = value * (1 - tolerance), value * (1 + tolerance)
    results_approximate = db.look_up(low, high, unitid=unitid, unittypeid=unittypeid)

    # Double value
    results_double = db.look_up(low * 2, high * 2, unitid=unitid, unittypeid=unittypeid)

    # Half
    results_half = db.look_up(low // 2, high // 2, unitid=unitid, unittypeid=unittypeid)

    # === ORDER OF MAGNITUDE MATCHES ===

    order = math.floor(math.log10(value))
    low, high = 10 ** order, 10 ** (order + 1)
    results_magnitude = db.look_up(low, high, unitid=unitid, unittypeid=unittypeid)

    # === COMPILATION ===

    results = []

    for r in results_exact:
        results.append(
            {
                "score": 0,
                "description": r[0],
                "value": float(r[1]),
                "unittypeid": int(r[2]),
                "unit": r[3],
                "why": "Exact match",
            }
        )

    for r in results_approximate:
        results.append(
            {
                "score": 2,
                "description": r[0],
                "value": float(r[1]),
                "unittypeid": int(r[2]),
                "unit": r[3],
                "why": "Approximate match",
            }
        )

    for r in results_double:
        results.append(
            {
                "score": 3,
                "description": r[0],
                "value": float(r[1]),
                "unittypeid": int(r[2]),
                "unit": r[3],
                "why": "Half of",
            }
        )

    for r in results_half:
        results.append(
            {
                "score": 3,
                "description": r[0],
                "value": float(r[1]),
                "unittypeid": int(r[2]),
                "unit": r[3],
                "why": "Double of",
            }
        )

    for r in results_magnitude:
        results.append(
            {
                "score": 6,
                "description": r[0],
                "value": float(r[1]),
                "unittypeid": int(r[2]),
                "unit": r[3],
                "why": "Same order of magnitude",
            }
        )

    idx = -1
    for r in results:
        # TODO error depends on type - double/half are off
        idx += 1
        absolute_error = abs(r["value"] - value)
        relative_error = absolute_error / max(value, r["value"])
        unittype_penalty = 1
        if r["unit"] != "none":
            unittype_penalty = 0 if r["unittypeid"] == unittypeid else 3

        r["absolute_error"] = round(absolute_error, 2)
        r["relative_error"] = round(relative_error, 2)
        r["score"] = round(r["score"] + relative_error + unittype_penalty, 2)
        r["id"] = idx

    # === FINISH ===

    # Remove doubles
    remove_doubles(results)

    # Sort results based on score
    results.sort(key=lambda r: r["score"])

    # Done!
    return results
