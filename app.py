from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():

	results = mongo.db.mars_app.find_one()
	return render_template("index.html", m_data = results)

    
# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
	mars_data = scrape_mars.scrape_mars()
	mongo.db.mars_app.update({}, mars_data, upsert=True)

	return redirect("/")

  
if __name__ == "__main__":
    app.run(debug=True)
