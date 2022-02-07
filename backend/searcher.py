from .database import Database


def search(original_value: int, unitid: int, unittypeid: int, categoryid: int):
    if not unitid:
        return []

    # Setup database
    db = Database()

    # Convert to proper SI unit
    if unitid not in db.get_si_units:
        factor = db.get_conversion_factor(unitid)
        value = original_value * factor
    else:
        value = original_value

    # Look for exact match with unit
    results_exact_unit = db.look_up(value, unittypeid)

    # Look for exact match without unit
    results_exact_general = db.look_up(value)

    # Look for approximate match (10%)
    results_approximate = db.look_up(value, unittypeid, tolerance=0.1)

    # Look for double
    results_double = db.look_up(value * 2, unittypeid, tolerance=0.1)

    # Look for half
    results_half = db.look_up(value // 2, unittypeid, tolerance=0.1)

    # TODO perform other searches

    results = []

    for r in results_exact_unit:
        results.append({
            'score': 0,
            'value': int(r[1]),
            'unit': r[2],  # TODO convert to proper unit name
            'description': r[3],
            'why': 'Exact match'
        })

    for r in results_exact_general:
        results.append({
            'score': 1,
            'value': int(r[1]),
            'unit': r[2],  # TODO convert to proper unit name
            'description': r[3],
            'why': 'Exact match'
        })

    for r in results_approximate:
        results.append({
            'score': 10,  # TODO compute score properly (related to distance)
            'value': int(r[1]),
            'unit': r[2],  # TODO convert to proper unit name
            'description': r[3],
            'why': 'Approximate match'
        })

    for r in results_double:
        results.append({
            'score': 12,  # TODO compute score properly (related to distance)
            'value': int(r[1]),
            'unit': r[2],  # TODO convert to proper unit name
            'description': r[3],
            'why': 'Double'
        })

    for r in results_half:
        results.append({
            'score': 13,  # TODO compute score properly (related to distance)
            'value': int(r[1]),
            'unit': r[2],  # TODO convert to proper unit name
            'description': r[3],
            'why': 'Half'
        })

    # TODO Remove doubles

    # Sort results based on score
    results.sort(key = lambda r: r['score'])

    # Done!
    return results