import requests, json
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from backend.util import convertNamesToLowerCase, convertMonthToNumber

class Scraper(ABC):

    url: str
    file_path: str
    state: BeautifulSoup = None

    def __get_soup(self) -> BeautifulSoup:
        try:
            response = requests.get(self.url)

        except requests.exceptions.ConnectionError:
            print(f"Error: could not reach {self.url}, arboting...")
            return

        if response.status_code == 200:
            return BeautifulSoup(response.text, "html.parser")
        else:
            print(f"Did not get proper response from {self.url}, arborting...")
            return

    @abstractmethod
    def _get_race_data(self, soup: BeautifulSoup) -> list:
        pass

    def __write_scraped_data(self, race_data: list):
        with open(self.file_path, 'w') as json_file:
            json.dump(race_data, json_file)
    
    def scrape(self):
        soup = self.__get_soup()
        # Bail out if the website has not changed since last scrape
        if soup == self.state:
            print("No change in data, arboting scrape!")
            return
        self.state = soup
        races = self._get_race_data(soup)
        self.__write_scraped_data(races)

class CyclingScraper(Scraper):

    def __init__(self):
        self.url = "https://www.procyclingstats.com/races.php"
        self.file_path = "backend/cycling_data.json"
    
    def _get_race_data(self, soup: BeautifulSoup) -> list:
        # Find the table rows with relevant race data
        rows = soup.select(".table-cont table tbody tr")

        races = []

        # Loop through the rows and extract the data
        for row in rows:
            date = row.select_one("td.cu500").get_text(strip=True)
            race_name = row.select("td")[2].get_text(strip=True)
            winner = row.select("td")[3].get_text(strip=True)

            # If there is no winner break from the loop and define the race to be the upcoming race
            if winner == "":
                upcoming_race = ({"Date": date, "Race": race_name})

                races.append(upcoming_race)
                break

            # Append scraped data to list
            races.append({"Date": date, "Race": race_name, "Winner": convertNamesToLowerCase(winner)})
        return races

class F1Scraper(Scraper):
    def __init__(self):
        self.url = "https://gpracingstats.com/"
        self.file_path = "backend/f1_data.json"

    def _get_race_data(self, soup: BeautifulSoup) -> list:
        # Find the table rows with relevant race data
        rows = soup.find("h2", text="F1 2023 winners").find_next("table").select("tbody tr")

        races = []
        
        for row in rows:
            if grand_prix := row.select_one("a"):
                gp_text = grand_prix.get_text(strip=True)
            if winner := grand_prix:
                winner_text = winner.find_next("a").get_text(strip=True)

            # If there was a winner append the data to races and continue
            if winner:
                races.append({"Race": gp_text, "Winner": winner_text})
                continue

            # There was not any winner so either the grand prix was cancelled or we have reached the upcoming grand prix
            gp_text = row.select_one("td").find_next().get_text(strip=True)
            date_text = row.select_one("td").find_next().findNext().get_text(strip=True)

            # If the grand prix was cancelled we continue
            if date_text == "Cancelled":
                continue

            # It was not the cancelled race and thus it must be the upcoming race
            upcoming_race = ({"Date": convertMonthToNumber(date_text), "Race": gp_text})

            # Append upcoming race to races
            races.append(upcoming_race)

            # We have defined the upcoming race data and the grand prix was not cancelled so no more scraping
            break
        return races