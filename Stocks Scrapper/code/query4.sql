query = """
SELECT location from companies
"""
c.execute(query)
r = c.fetchall()
r = list(dict.fromkeys(r))
query_4 = {}
for location in r:
    query = """
    SELECT DISTINCT name FROM companies WHERE location = ?
    """
    c.execute(query, location)
    query_4[f'{location[0]}'] = c.fetchall()