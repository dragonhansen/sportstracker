import http.server
import socketserver
import schedule
import time
from scraper import scrape_gprs, scrape_pcs

# Specify the directory where your HTML and other static files are located
directory = "html"

# Set the port number for your web server
port = 8000

# Create a web server that serves files from the specified directory
Handler = http.server.SimpleHTTPRequestHandler

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

# Start the scheduler thread
import threading
schedule_thread = threading.Thread(target=schedule_thread)
schedule_thread.daemon = True
schedule_thread.start()

with socketserver.TCPServer(("", port), Handler) as httpd:
    print(f"Serving at port {port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer is shutting down.")
