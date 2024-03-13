query = """
SELECT symbol,MAX(price/avg_price) FROM quotes
"""
c.execute(query)
r = c.fetchall()
r = r[0][0]
query = """
SELECT name FROM companies WHERE symbol = ?
"""
c.execute(query, (r,))
r = c.fetchall()
print(r[0][0])
