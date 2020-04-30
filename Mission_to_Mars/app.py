from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scraper_mars

app = Flask(__name__)

#mongo setup
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

@app.route("/")
def index():    
    data = mongo.db.data.find_one()
    return render_template("index.html", data=data)


@app.route("/scrape")
def scrape():
    data = scraper_mars.scrape()
    mongo.db.data.update({}, data, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)