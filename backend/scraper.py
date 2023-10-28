import requests, json
from bs4 import BeautifulSoup

def scrape_pcs():
    # URL of the page to scrape
    url = "https://www.procyclingstats.com/races.php"

    try:
        # Send an HTTP GET request
        response = requests.get(url)

    except requests.exceptions.ConnectionError:
        print("Error: could not reach procyclingstats, arboting...")
        return

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all table rows (excluding the header row)
        rows = soup.select(".table-cont table tbody tr")

         # Initialize lists to store the scraped data from past races
        past_races = []

        # Loop through the rows and extract the data
        for row in rows:
            date = row.select_one("td.cu500").get_text(strip=True)
            race_name = row.select("td")[2].get_text(strip=True)
            winner = row.select("td")[3].get_text(strip=True)

            upcoming_race = None

            # If there is no winner break from the loop and define the race to be the upcoming race
            if winner == "":
                upcoming_race = ({"Date": date, "Race": race_name})
                break

            # Append scraped data to list
            past_races.append({"Date": date, "Race": race_name, "Winner": winner})

        # Define the file path where you want to save the JSON data
        file_path = "backend/cycling_data.json"

        # Open the file in write mode and save the data as JSON
        with open(file_path, 'w') as json_file:
            json.dump(past_races, json_file)
            if upcoming_race:
                json.dump(upcoming_race, json_file)

def scrape_gprs():
     # URL of the page to scrape
    url = "https://gpracingstats.com/"

    try:
        # Send an HTTP GET request
        response = requests.get(url)
    except requests.exceptions.ConnectionError:
        print("Error: could not reach gpracingstats, arboting...")
        return

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the F1 2023 Race winners container
        rows = soup.find("h2", text="F1 2023 winners").find_next("table").select("tbody tr")

        # Initialize lists to store the scraped data from past races
        past_races = []
        
        for row in rows:
            # Check if entires for grand prixs and winners exist and find the text if they do
            if grand_prix := row.select_one("a"):
                gp_text = grand_prix.get_text(strip=True)
            if winner := grand_prix:
                winner_text = winner.find_next("a").get_text(strip=True)

            # If there was a winner append the data to the past races list and continue
            if winner:
                past_races.append({"Race": gp_text, "Winner": winner_text})
                continue

            # There was not any winner so either the grand prix was cancelled or we have reached the upcoming grand prix
            # Find text for upcoming grand prix
            gp_text = row.select_one("td").find_next().get_text(strip=True)
            date_text = row.select_one("td").find_next().findNext().get_text(strip=True)

            # If we have been fooled and the grand prix was actully cancelled we continue
            if date_text == "Cancelled":
                continue

            upcoming_race = ({"Date": date_text, "Race": gp_text})

            # We have defined the upcoming race data and the grand prix was not cancelled so no more scraping
            break

        # Define the file path where you want to save the JSON data
        file_path = "backend/f1_data.json"

        # Open the file in write mode and save the data as JSON
        with open(file_path, 'w') as json_file:
            json.dump(past_races, json_file)
            if upcoming_race:
                pass
                #json.dump(upcoming_race, json_file)
        
scrape_pcs()
scrape_gprs()