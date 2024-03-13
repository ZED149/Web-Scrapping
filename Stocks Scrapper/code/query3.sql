query = """
SELECT symbol FROM quotes WHERE price > 30 AND price - avg_price
"""
c.execute(query)
r = c.fetchall()
my_list = []
for i in r:
    query = """
    SELECT name FROM companies WHERE symbol = ?
    """
    c.execute(query, (i[0], ))
    r = c.fetchall()
    my_list.append(r[0][0])