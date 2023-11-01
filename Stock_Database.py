import sqlite3
import stockprices

# Connect to the in-memory database, this is great for testing as it does not include only database values
#conn = sqlite3.connect(':memory:')

#this is great for keeping an up to date stock database with results from a previous time
conn = sqlite3.connect('stock.db')

c = conn.cursor()

# Define the SQL query to create the "stocks" table this will only be used for RAM memory storage
# create_table_query = """
# CREATE TABLE stocks (
#  symbol TEXT,
#  price REAL,
#  changeInDollars REAL,
#  changeInPercent REAL
# )
# """

# Execute the create table query for only if using RAM
#c.execute(create_table_query)

# Define the symbol
for s in stockprices.MyStocks:
 price = stockprices.getPrice(s)
 Cdollar = stockprices.getChangeInDollars(s)
 Cpercent = stockprices.getChangeInPercent(s)

 # Define the SQL query with placeholders for inserting data
 insert_query = "INSERT INTO stocks (symbol, price, changeInDollars, changeInPercent) VALUES (?,?,?,?)"

 # Execute the query to insert the data for the first stock
 with conn:
     c.execute(insert_query, (s, price, Cdollar, Cpercent))

# Commit the changes to the database
conn.commit()

# Query the database to retrieve the data for a specified symbol
#c.execute("SELECT * FROM stocks WHERE symbol = ?", (a,))

#query from all tables in database!
c.execute("SELECT * FROM stocks")

result = c.fetchall()
print(result)


def delete_entry():
    with conn:
        c.execute("DELETE * FROM stocks WHERE symbol=:symbol", {'symbol': 's'})
# Close the connection


conn.close()