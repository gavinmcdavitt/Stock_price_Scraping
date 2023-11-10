from flask import Flask, render_template, g
from matplotlib import pyplot as plt
import matplotlib
import sqlite3 as db
import io
import base64
import threading
import Stock_Database
from stockprices import MyStocks

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

        return graph_bytes


@app.route('/graphs')
def another_index():
    graph_data = [showgraph(symbol) for symbol in MyStocks]
    return render_template('index2.html', graph_data=graph_data)

# Define a route for the root URL that renders the 'index.html' template
@app.route('/')
def index():
    graph_data = graphforall()
    return render_template('index.html', graph_data=graph_data)
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
    return f"data:image/png;base64,{graph_bytes}"

def graphSingleStock(symbol):
    with app.app_context():
        conn = db.connect('new_stock_2.db', check_same_thread=False, isolation_level=None)
        c=conn.cursor()

    fig, ax = plt.subplots()
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

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    graph_bytes = base64.b64encode(buffer.getvalue()).decode('utf-8')
    zipped_data = list(zip(graph_bytes, MyStocks))
    return render_template('index2.html', zipped_data=zipped_data)

if __name__ == "__main__":
    app.run(debug=True, threaded = True)
    Stock_Database.automate_scraping()
