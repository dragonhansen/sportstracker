from http.server import HTTPServer, SimpleHTTPRequestHandler
import schedule
import time
import threading
from scraper import scrape_gprs, scrape_pcs

hostName = "localhost"
serverPort = 8000

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
    
    # Define parameters for the webserver
    handler = SimpleHTTPRequestHandler
    webServer = HTTPServer((hostName, serverPort), handler)
    print(f"Server started at {hostName}:{serverPort}")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")