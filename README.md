# Stock_price_Scraping
I made this project, to show how you can have python be used as a tool for automation. It's very fun and I think a really good show of my expertise in python. When you are downloading these files, make sure that you follow these steps:
step 1 open a blank folder in your perferred IDE. If you are on windows you will run these commands:
Step 2 run these commands below to ensure that you have the correct environment:

py -3 -m venv {Name of your environment}
and then to activate your environment:
{Name of your environment}\Scripts\activate

If you are on Mac/Linux:
python3 -m venv {Name of your environment}
to activate your environment:
. {Name of your environment}/bin/activate

You must do this so you can ensure that your installed libraries are not installed globally on your system. you should see a (venv) or (name of your environment) next to your name in terminal.
step 3:
Move all of these files into your blank folder. With the the 2 files index.html and index2.html you will need to put that into a directory called 'templates'. Place that templates folder into your project directory.
step 4:
run this command to install all dependencies onto your project.
pip install -r requirements.txt
step 5:
run this command to install flask.
pip install flask
step 6:
run app.py or 'python app.py' to allow your flask framework to be running.
step7: Go to localhost:5000 in your URL.
If any of that is way too confusing I have a video that you can watch to see how I did it myself in VSCode.
https://www.dropbox.com/scl/fi/z814qqkk300obot1ab7ft/chrome_FwePZEtTaD.mp4?rlkey=4v7nb4ad99dga8klblbf6rkxk&dl=0


If you want to use different stocks than the ones I have chosen, you must remember that:
-All stock symbols must be capitalized. If it is not capitalized your program will not work at all.
-Any changes to list MyStocks: must then have a completely new database. To change the name of your database go to stock_database.py and change the first parameter of the database in line:
conn = sqlite3.connect('new_stock_2.db', check_same_thread=False, isolation_level=None) 
to something that is different. This way it will store all of the stock data with different names.

One your flask is running it will automatically scrape for more stock data every 15 minutes (as to not flood Yahoo Finance with large amounts of http requests). I hope this helps and can explain the project more throughly. 
