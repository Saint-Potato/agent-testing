import json

def parse_records(records):
    results = []

    for row in records:
        results.append({
            "id": row[0],
            "data": json.loads(row[1])   # Exception is no longer handled
        })

    return results
