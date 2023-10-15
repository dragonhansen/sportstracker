import requests
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

            # If there is no winner break from the loop and define the race to be the upcoming race
            if winner == "":
                upcoming_race = ({"Date": date, "Race Name": race_name})
                break

            # Append scraped data to list
            past_races.append({"Date": date, "Race Name": race_name, "Winner": winner})
        
        try:
            # Create HTML for upcoming race
            html_upcoming_race = "<table><h2>Next Race</h2><thead><tr><th>Date</th><th>Race Name</th></tr></thead><tbody>"
            html_upcoming_race += f"<tr><td>{upcoming_race['Date']}</td><td>{upcoming_race['Race Name']}</td></tr>"
            html_upcoming_race += "</tbody></table>"


            # Create HTML table for past races
            html_table = "<table><h2>Finished Races</h2><thead><tr><th>Date</th><th>Race Name</th><th>Winner</th></tr></thead><tbody>"

            # Insert data into the table
            for data in past_races:
                html_table += f"<tr><td>{data['Date']}</td><td>{data['Race Name']}</td><td>{data['Winner']}</td></tr>"

            # Finish HTML table with the right tags
            html_table += "</tbody></table>"

            # Write the scraped data to HTML file
            write_scraped_data("html/scraped_data_cycling.html", html_upcoming_race, html_table)

        except UnboundLocalError:
            print("Error: could net scrape PCS data properly, aborting...")

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

        past_races = []

        for row in rows:
            if grand_prix := row.select_one("a"):
                gp_text = grand_prix.get_text(strip=True)
            if winner := grand_prix:
                winner_text = winner.find_next("a").get_text(strip=True)
                past_races.append({"Race": gp_text, "Winner": winner_text})
                continue
            upcoming_race = row.select_one("td").find_next()
            upcoming_text = upcoming_race.get_text(strip=True)
            if upcoming_text != "Emilia Romagna":
                date_text = upcoming_race.find_next("td").get_text(strip=True)
                break

        try:
            # Create HTML for upcoming race
            html_upcoming_race = "<table><h2>Next Grand Prix</h2><thead><tr><th>Date</th><th>Race Name</th></tr></thead><tbody>"
            html_upcoming_race += f"<tr><td>{date_text}</td><td>{upcoming_text}</td></tr>"
            html_upcoming_race += "</tbody></table>"

            # Create HTML table for past races
            html_table = "<table><h2>Finished GP's</h2><thead><th>Race Name</th><th>Winner</th></tr></thead><tbody>"

            # Insert data into the table
            for data in past_races:
                html_table += f"<tr><td>{data['Race']}</td><td>{data['Winner']}</td></tr>"

            # Finish HTML table with the right tags
            html_table += "</tbody></table>"

            # Write the scraped data to HTML file
            write_scraped_data("html/scraped_data_f1.html", html_upcoming_race, html_table)

        except UnboundLocalError:
            print("Error: could net scrape F1 data properly, aborting...")

def write_scraped_data(html_file: str, upcoming: str, past: str):
    # Read the existing content of the scraped_data.HTML file
        with open(html_file, "r", encoding='UTF-8') as file:
            existing_content = file.read()

        # Insert the two new HTML tables inside scraped_data.HTML
        with open(html_file, "w", encoding="UTF-8") as file:
            position_begin = existing_content.find("<body>") + len("<body>")
            position_end = existing_content.find("</body>")
            if position_begin != -1 and position_end != -1:
                file.write(existing_content[:position_begin])
                file.write(upcoming)
                file.write(past)
                file.write(existing_content[position_end:])
        
scrape_pcs()
scrape_gprs()