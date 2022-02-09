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
    if unitid not in db.get_si_units:
        factor = db.get_conversion_factor(unitid)
        value = original_value * factor
    else:
        value = original_value

    # === EXACT MATCHES ===

    # Look for exact match
    results_exact = db.look_up(value)

    # === APPROXIMATE MATCHES (10%) ===

    # Approximate near
    tolerance = 0.101
    low, high = value * (1 - tolerance), value * (1 + tolerance)
    results_approximate = db.look_up(low, high)

    # Double value
    results_double = db.look_up(low * 2, high * 2)

    # Half
    results_half = db.look_up(low // 2, high // 2)

    # === ORDER OF MAGNITUDE MATCHES ===

    order = math.floor(math.log10(value))
    low, high = 10 ** order, 10 ** (order + 1)
    results_magnitude = db.look_up(low, high)

    # === COMPILATION ===
    # TODO update below and proper why depending on unit match
    # TODO convert to proper unit name
    # TODO also include relative and absolute error

    results = []

    for r in results_exact:
        results.append(
            {
                "score": 0,
                "value": int(r[1]),
                "unit": r[2],  # TODO convert to proper unit name
                "description": r[3],
                "why": "Exact match (unit or not)",  # TODO
            }
        )

    for r in results_approximate:
        results.append(
            {
                "score": 10,  # TODO compute score properly (related to distance)
                "value": int(r[1]),
                "unit": r[2],  # TODO convert to proper unit name
                "description": r[3],
                "why": "Approximate match",
            }
        )

    for r in results_double:
        results.append(
            {
                "score": 12,  # TODO compute score properly (related to distance)
                "value": int(r[1]),
                "unit": r[2],  # TODO convert to proper unit name
                "description": r[3],
                "why": "Double",
            }
        )

    for r in results_half:
        results.append(
            {
                "score": 13,  # TODO compute score properly (related to distance)
                "value": int(r[1]),
                "unit": r[2],  # TODO convert to proper unit name
                "description": r[3],
                "why": "Half",
            }
        )

    for r in results_magnitude:
        results.append(
            {
                "score": 20,  # TODO compute score properly (related to distance)
                "value": int(r[1]),
                "unit": r[2],  # TODO convert to proper unit name
                "description": r[3],
                "why": "Same order of magnitude",
            }
        )

    # === FINISH ===

    # Remove doubles
    remove_doubles(results)

    # Sort results based on score
    results.sort(key=lambda r: r["score"])

    # Done!
    return results
