import requests, json
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from backend.util import convertNamesToLowerCase, convertMonthToNumber

class Scraper(ABC):

    url: str
    soup: BeautifulSoup
    state: BeautifulSoup
    past_races: list
    upcoming_race: dict
    file_path: str

    def getSoup(self):
        try:
            # Send an HTTP GET request
            response = requests.get(self.url)

        except requests.exceptions.ConnectionError:
            print(f"Error: could not reach {self.url}, arboting...")
            return

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content of the page
            self.soup = BeautifulSoup(response.text, "html.parser")

            return

            # Bail out if the website has not changed since last scrape
            if self.state == self.soup:
                print("No change in data, arboting scrape!")
                return
            self.state = self.soup

    @abstractmethod
    def scrape(self):
        pass

    def write_scraped_data(self, race_data: list):
        # Open the file in write mode and save the data as JSON
        with open(self.file_path, 'w') as json_file:
            json.dump(race_data, json_file)
    
    def main(self):
        self.getSoup()
        self.scrape()
        self.write_scraped_data(self.past_races)

class CyclingScraper(Scraper):

    def __init__(self):
        self.url = "https://www.procyclingstats.com/races.php"
        self.file_path = "backend/cycling_data.json"
    
    def scrape(self):
        # Find all table rows (excluding the header row)
        rows = self.soup.select(".table-cont table tbody tr")

        # Initialize lists to store the scraped data from past races
        self.past_races = []

        # Loop through the rows and extract the data
        for row in rows:
            date = row.select_one("td.cu500").get_text(strip=True)
            race_name = row.select("td")[2].get_text(strip=True)
            winner = row.select("td")[3].get_text(strip=True)

            self.upcoming_race = None

            # If there is no winner break from the loop and define the race to be the upcoming race
            if winner == "":
                self.upcoming_race = ({"Date": date, "Race": race_name})

                # Append upcoming race to past races bacuse we only dump one JSON file
                self.past_races.append(self.upcoming_race)
                break

            # Append scraped data to list
            self.past_races.append({"Date": date, "Race": race_name, "Winner": convertNamesToLowerCase(winner)})

class F1Scraper(Scraper):
    def __init__(self):
        self.url = "https://gpracingstats.com/"
        self.file_path = "backend/f1_data.json"

    def scrape(self):
        # Find the F1 2023 Race winners container
        rows = self.soup.find("h2", text="F1 2023 winners").find_next("table").select("tbody tr")
        # Initialize lists to store the scraped data from past races
        self.past_races = []
        
        for row in rows:
            # Check if entires for grand prixs and winners exist and find the text if they do
            if grand_prix := row.select_one("a"):
                gp_text = grand_prix.get_text(strip=True)
            if winner := grand_prix:
                winner_text = winner.find_next("a").get_text(strip=True)

            # If there was a winner append the data to the past races list and continue
            if winner:
                self.past_races.append({"Race": gp_text, "Winner": winner_text})
                continue

            # There was not any winner so either the grand prix was cancelled or we have reached the upcoming grand prix
            # Find text for upcoming grand prix
            gp_text = row.select_one("td").find_next().get_text(strip=True)
            date_text = row.select_one("td").find_next().findNext().get_text(strip=True)

            # If we have been fooled and the grand prix was actully cancelled we continue
            if date_text == "Cancelled":
                continue

            self.upcoming_race = ({"Date": convertMonthToNumber(date_text), "Race": gp_text})

            # Append upcoming race to past races bacuse we only dump one JSON file
            self.past_races.append(self.upcoming_race)

            # We have defined the upcoming race data and the grand prix was not cancelled so no more scraping
            break