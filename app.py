from flask import Flask, render_template, url_for, redirect, jsonify, json, request
from apscheduler.schedulers.background import BackgroundScheduler
from backend.Scraper import CyclingScraper, F1Scraper

app = Flask(__name__, template_folder='frontend/dist', static_folder='frontend/dist/assets')

cycling_scraper = CyclingScraper()
f1_scraper = F1Scraper()

scheduler = BackgroundScheduler()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/get-data-cycling', methods=['GET'])
@app.route('/get-data-f1', methods=['GET'])
def get_data():

    # Use request to get endpoint
    endpoint = request.path

    # Specify the path to your JSON file depending on the endpoint
    if endpoint == '/get-data-cycling':
        json_file_path = 'backend/cycling_data.json'
    else:
        json_file_path = 'backend/f1_data.json'

    try:
        with open(json_file_path, 'r') as json_file:
            # Load the JSON data from the file
            data = json.load(json_file)
            
            # Use jsonify to create a JSON response
            return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "File not found"})


# Define a function to run the scraper
def run_scraper():
    print("Running the scraper...")
    cycling_scraper.scrape()
    f1_scraper.scrape()
    print("Scraper finished")

scheduler.add_job(run_scraper, "interval", seconds=900)
scheduler.start()

if __name__ == "__main__": 
    app.run(debug=False, host="0.0.0.0", port=8000)