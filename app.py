from flask import Flask, render_template, url_for, request, redirect, jsonify
from datetime import datetime

import stockprices
app = Flask(__name__)

#GOAL: Once you have the database properly running you can input the data into flask to output
#it and make some graphs of the data.
@app.route('/')
def get_stock_data():
    return jsonify(stockprices.StockData)

if __name__ =="__main__":
    app.run(debug=True)
    get_stock_data()