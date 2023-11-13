import sqlite3
import stockprices
import time
import datetime
import threading
# this is great for keeping an up to date stock database with results from a previous time
conn = sqlite3.connect('new_stock_2.db', check_same_thread=False, isolation_level=None)
c = conn.cursor()
'''''''''''
#TESTING CODE DO NOT ADD TO DATABASE
# Connect to the in-memory database, this is great for testing as it does not include only database values
#conn = sqlite3.connect(':memory:')
# Define the SQL query to create the "stocks" table this will only be used for RAM memory storage

# 
# # Execute the create table query for only if using RAM
'''''''''''
#Creates a table that will have the following data, I decided to always have all of the data be scraped in case,
#it may be used later.
create_table_query = """
CREATE TABLE IF NOT EXISTS stocks (
symbol TEXT,
price REAL,
changeInDollars REAL,
changeInPercent REAL,
openat REAL,
peratio REAL,
marketcap REAL,
dailyrange REAL
)
 """
c.execute(create_table_query)
# Define the symbol
#This one function calls the previous functions made in stockprices.py, I then create an sqlite3 query and place the
#data in the databse.
def StockInfo():
    for s in stockprices.MyStocks:
        price = stockprices.getPrice(s)
        Cdollar = stockprices.getChangeInDollars(s)
        Cpercent = stockprices.getChangeInPercent(s)
        openAt = stockprices.getOpenAt(s)
        PERatio = stockprices.getPERatio(s)
        marketCap = stockprices.getMarketCap(s)
        dailyR = stockprices.getDailyRange(s)

        # Define the SQL query with placeholders for inserting data
        insert_query = "INSERT INTO stocks (symbol, price, changeInDollars, changeInPercent, openat, peratio, marketcap, dailyrange) " \
                       "VALUES (?,?,?,?,?,?,?,?)"

        # Execute the query to insert the data for the first stock
        with conn:
            c.execute(insert_query, (s, price, Cdollar, Cpercent, openAt, PERatio, marketCap, dailyR))

    # Commit the changes to the database
    conn.commit()
#A simplete delete function to organize the databse at a later time, if the data seems to be manipulated/incorrect.
def delete_entry(symbol, s):
    with conn:
        c.execute("DELETE FROM stocks WHERE symbol=:symbol", {'symbol': 's'})


#this function allows for multiple threads to be connected to our sqlite3 database. I use this to display the different
#graphs on localhost:5000 and localhost:5000/graphs
def write_thread():
    while True:
        with conn:
            now = datetime.datetime.now()

            # Check if it's a weekday (Monday to Friday)
            if now.weekday() < 5:
                # Check if the current time is between 10:00 AM and 4:00 PM Eastern Standard Time
                if datetime.time(10, 0) <= now.time() <= datetime.time(16, 0):
                    StockInfo()
                    print("automating")
                else:
                    print("sleeping")
        # Sleep for an interval before the next iteration
        time.sleep(900)

# Start the write thread when the stock_database.py is run
write_thread = threading.Thread(target=write_thread)
write_thread.start()

#to stop the flask application press CTRL + C (windows) or Command + C (MAC)
if __name__ == "__main__":
    try:
        pass
    except KeyboardInterrupt:
        conn.close()

