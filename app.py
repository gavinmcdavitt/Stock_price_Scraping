from flask import Flask, render_template, g
from matplotlib import pyplot as plt
import matplotlib
import sqlite3 as db
import io
import base64
import threading
import Stock_Database
from stockprices import MyStocks
#These three lines will allow for a flask application to be created, use of multiple graphs, and connect to our
#databse.
matplotlib.use('Agg')
app = Flask(__name__)
app.config['DATABASE'] = 'new_stock_2.db'

# Function to get the database connection
def get_db():
    if 'db' not in g:
        g.db = db.connect(app.config['DATABASE'], check_same_thread=False)
    return g.db

# Close the database connection when the request is finished
@app.teardown_appcontext
def close_db(error =None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

#this function is used to graph multiple plots, all in their own graphs. It has been written so that it can be looped
#through with our stock list. As long as previous stock data had been scraped, it can be outputted.
#the first segment creates a connection to the database, the second segment creates a graph of the stock data.
#The third segment allow for the graph to be encoded in base64, so that it can dynamically change everytime the page
#reloads.
def showgraph(symbol):
    with app.app_context():
        conn = db.connect('new_stock_2.db', check_same_thread=False, isolation_level=None)
        c = conn.cursor()

        fig, ax = plt.subplots()
        query = "SELECT price FROM stocks WHERE symbol = ?"
        c.execute(query, (symbol,))
        data = c.fetchall()
        y_values = [row[0] for row in data]
        x_values = range(1, len(data) + 1)
        ax.plot(x_values, y_values, label=symbol)
        ax.set_title(f'Stock Price for {symbol}')
        ax.set_xlabel('Data Point Index')
        ax.set_ylabel('Price')
        ax.legend()

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        plt.close()
        graph_bytes = base64.b64encode(buffer.getvalue()).decode('utf-8')
        close_db()
        return graph_bytes

#This creates a flask framework, and allows for the stock symbols to be looped through, and given a variable name.
#I then return the data to index2.html, and inside index2.html, it will loop through the data, to display the graphs.
@app.route('/graphs')
def another_index():
    graph_data = [showgraph(symbol) for symbol in MyStocks]
    return render_template('index2.html', graph_data=graph_data)

# Define a route for the root URL that renders the 'index.html' template
@app.route('/')
def index():
    graph_data = graphforall()
    return render_template('index.html', graph_data=graph_data)
#for this function it simply creates a graph with multiple stocks in one graph. I decided to make a graph that
#has multiple stock symbols on it. In the stock data that I had scraped I had a few stocks that were similar in price
#and can be effective to show. The 4 stocks, I chose were META, GOOGLE, APPLE, and Tesla. I loop through each stock,
#and place them on the same graph.
def graphforall():
    # In this code, one graph should plot 4 tech stock plots.
    with app.app_context():
        conn = db.connect('new_stock_2.db', check_same_thread=False, isolation_level=None)
        c = conn.cursor()

    tech_stocks = ["META", "GOOGL", "AAPL", "TSLA"]
    fig, ax = plt.subplots(figsize=(10, 6))
    for symbol in tech_stocks:
        query = "SELECT price FROM stocks WHERE symbol = ?"
        c.execute(query, (symbol,))
        data = c.fetchall()
        y_values = [row[0] for row in data]
        x_values = range(1, len(data) + 1)
        ax.plot(x_values, y_values, label=symbol)
        ax.set_title(f'Stock Price for Tech Stocks')
        ax.set_xlabel('Data Point Index')
        ax.set_ylabel('Price')
        ax.legend()
    custom_y_ticks = [value for value in range(100, 325, 25)]
    ax.set_yticks(custom_y_ticks)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    graph_bytes = base64.b64encode(buffer.getvalue()).decode('utf-8')
    close_db()
    return f"data:image/png;base64,{graph_bytes}"

#This commented code, was code that I had used earlier, but now no longer need. I did not want to delete it, in case
#I could need this for later.

# def graphSingleStock(symbol):
#     with app.app_context():
#         conn = db.connect('new_stock_2.db', check_same_thread=False, isolation_level=None)
#         c=conn.cursor()
#
#     fig, ax = plt.subplots()
#     query = "SELECT price FROM stocks WHERE symbol = ?"
#     c.execute(query, (symbol,))
#     data = c.fetchall()
#     y_values = [row[0] for row in data]
#     x_values = range(1, len(data) + 1)
#     ax.plot(x_values, y_values, label=symbol)
#     ax.set_title(f'Stock Price for Tech Stocks')
#     ax.set_xlabel('Data Point Index')
#     ax.set_ylabel('Price')
#     ax.legend()
#
#     buffer = io.BytesIO()
#     plt.savefig(buffer, format='png')
#     plt.close()
#     graph_bytes = base64.b64encode(buffer.getvalue()).decode('utf-8')
#     zipped_data = list(zip(graph_bytes, MyStocks))
#     return render_template('index2.html', zipped_data=zipped_data)

if __name__ == "__main__":
    app.run(debug=True, threaded = True)
    Stock_Database.write_thread()
