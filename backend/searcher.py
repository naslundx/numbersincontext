from .database import Database

def search(value: int, unit: str, category: str):
    # Setup database
    db = Database()

    # TODO convert to proper SI unit

    # Look for exact match with unit
    results_exact_unit = db.look_up(value, unit)

    # Look for exact match without unit
    # results_exact_general = db.look_up(value)

    # Look for approximate match (10%)
    results_approximate = db.look_up(value, unit, tolerance=0.1)

    # Look for double
    results_double = db.look_up(value * 2, unit, tolerance=0.1)

    # Look for half
    results_half = db.look_up(value // 2, unit, tolerance=0.1)

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