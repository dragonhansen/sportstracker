from flask import Flask, render_template
import schedule
import time
import threading
from scraper import scrape_gprs, scrape_pcs

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

# Define a function to run the scraper at set intervals
def run_scraper():
    print("Running the scraper...")
    scrape_pcs()
    scrape_gprs()
    print("Scraper finished")

# Schedule the scraper to run every hour (adjust as needed)
schedule.every(900).seconds.do(run_scraper)

# Start a separate thread for the scheduler
def schedule_thread():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":    
    # Start the scheduler thread
    schedule_thread = threading.Thread(target=schedule_thread)
    schedule_thread.daemon = True
    schedule_thread.start()

    app.run(debug=True, host='localhost', port=8000)