from flask import Flask, render_template, request, url_for, redirect
import time
from apscheduler.schedulers.background import BackgroundScheduler
from scraper import scrape_gprs, scrape_pcs

app = Flask(__name__)

scheduler = BackgroundScheduler()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/trigger-scraper', methods=['POST'])
def trigger_scraper():
    run_scraper()
    return redirect(url_for('index'))

# Define a function to run the scraper
def run_scraper():
    print("Running the scraper...")
    scrape_pcs()
    scrape_gprs()
    print("Scraper finished")

scheduler.add_job(run_scraper, "interval", seconds=900)
scheduler.start()

if __name__ == "__main__": 
    app.run(debug=True, host="localhost", port=8000)