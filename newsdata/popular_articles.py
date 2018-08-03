#!/usr/bin/env python
import psycopg2

# Global variables
DBNAME = "news"
TOP_COUNT = 3

# connect to database
db = psycopg2.connect(database=DBNAME)

# open cursor to perform database operations
cur = db.cursor()

'''
Constructing sql queries
'''

final_query = """
SELECT title,
       num
FROM articles
JOIN
  (SELECT count(*) AS num,
          reverse(split_part(reverse(PATH), '/', 1)) AS log_slug
   FROM log
   GROUP BY reverse(split_part(reverse(PATH), '/', 1))
   ORDER BY num DESC) AS log_query ON articles.slug = log_query.log_slug
"""

# Getting all queries
cur.execute(final_query)
results = cur.fetchall()


'''
popular articles
'''
# print out header information - popular articles
print("")
print("The most popular " + str(TOP_COUNT) + " articles of all time are:")

# print out top viewed articles
count = 0
for row in results:
    if count == TOP_COUNT:
        break
    print(row[0] + " -- " + str(row[1]) + " views.")
    count += 1
print("")

# end session
cur.close
db.close
