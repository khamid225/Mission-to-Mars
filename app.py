from flask import Flask, render_template
from flask_pymongo import PyMongo

import scrapping

app = Flask(__name__)

# Change user/password if needed
dbuser = 'x'
passw = 'x'

mongo_server = "mongodb+srv://{}:{}@cluster0.9b2o3.mongodb.net/mars_app".format(dbuser, passw)
app.config["MONGO_URI"] = mongo_server
mongo = PyMongo(app)

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scrapping.scrape_all()
    mars.update({}, mars_data, upsert=True)
    return "Scraping Successful!"

if __name__ == "__main__":
    app.run(debug=True)
