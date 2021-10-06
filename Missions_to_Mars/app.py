from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create instance of Flask
app = Flask(__name__)

# Create Mongo Connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Create Routes

@app.route("/scrape")
def scrape():
    mars_scrape = scrape_mars.scrape()
    mongo.db.collection.update({},mars_scrape, upsert=True)
    return "Scraping successful!"

@app.route("/")
def home():
     mars_data = mongo.db.collection.find_one()
     return render_template("index.html",redplanet=mars_data)

if __name__ == "__main__":
    app.run()
