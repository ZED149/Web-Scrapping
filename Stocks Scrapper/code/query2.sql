query = """
SELECT symbol,MAX(price) FROM quotes WHERE avg_price<close
"""
c.execute(query)
r = c.fetchall()
r = r[0][0]
query = """
SELECT name FROM companies WHERE symbol = ?
"""
c.execute(query, (r, ))
r = c.fetchall()
