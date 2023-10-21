from flask import Flask, render_template, request, url_for, redirect
import time
from apscheduler.schedulers.background import BackgroundScheduler
from scraper import scrape_gprs, scrape_pcs

class Webapp:

    app = Flask(__name__)

    def __init__(self) -> None:
        # Schedule the scraper to run at set intervals
        scheduler = BackgroundScheduler()
        scheduler.add_job(Webapp.run_scraper, "interval", seconds=10)
        scheduler.start()

    @app.route('/')
    def index():
        return render_template("index.html")

    @app.route('/trigger-scraper', methods=['POST'])
    def trigger_scraper():
        Webapp.run_scraper()
        return redirect(url_for('index'))

    # Define a function to run the scraper
    def run_scraper():
        print("Running the scraper...")
        scrape_pcs()
        scrape_gprs()
        print("Scraper finished")

    
if __name__ == "__main__": 
    webapp = Webapp()   
    webapp.app.run(debug=True, host="0.0.0.0", port=8000)