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

            # Define upcoming race regardless if season is finished so we can switch on the parameter later
            upcoming_race = None

            # If there is no winner break from the loop and define the race to be the upcoming race
            if winner == "":
                upcoming_race = ({"Date": date, "Race Name": race_name})
                break

            # Append scraped data to list
            past_races.append({"Date": date, "Race Name": race_name, "Winner": winner})
        
        try:
            table_upcoming = ""
            if upcoming_race:
                table_upcoming += "<table><h2>Next Race</h2><thead><tr><th>Date</th><th>Race Name</th></tr></thead>"
                table_upcoming += f"<tbody><tr><td>{data['Date']}</td><td>{data['Race Name']}</td></tr>"
                table_upcoming += "</tbody></table>"
            
            table_previous = ""
            table_previous += "<table><h2>Finished Races</h2><thead><tr><th>Date</th><th>Race Name</th><th>Winner</th></tr></thead>"
            table_previous += "<tbody>"
            for data in past_races:
                table_previous += f"<tr><td>{data['Date']}</td><td>{data['Race Name']}</td><td>{data['Winner']}</td></tr>"

            table_previous += "</tbody></table>"

            html_table = table_upcoming+table_previous


            # Write the scraped data to HTML file
            write_scraped_data("templates/scraped_data_cycling.html", html_table)

        except UnboundLocalError as e:
            print(e)
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
            upcoming_race = row.select_one("td").find_next()
            upcoming_text = upcoming_race.get_text(strip=True)
            date_text = upcoming_race.find_next("td").get_text(strip=True)

            # If we have been fooled and the grand prix was actully cancelled we continue
            if date_text == "Cancelled":
                continue

            # We have defined the upcoming race data and the grand prix was not cancelled so no more scraping
            break

        try:
            table_upcoming = ""
            if date_text:
                table_upcoming += "<table><h2>Next Grand Prix</h2><thead><tr><th>Date</th><th>Grand Prix</th></tr></thead>"
                table_upcoming += f"<tbody><tr><td>{date_text}</td><td>{upcoming_text}</td></tr>"
                table_upcoming += "</tbody></table>"
            
            table_previous = ""
            table_previous += "<table><h2>Finished GP's</h2><thead><tr><th>Grand Prix</th><th>Winner</th></tr></thead>"
            table_previous += "<tbody>"
            for data in past_races:
                table_previous += f"<tr><td>{data['Race']}</td><td>{data['Winner']}</td></tr>"

            table_previous += "</tbody></table>"

            html_table = table_upcoming+table_previous

            
            write_scraped_data("templates/scraped_data_f1.html", html_table)

        except UnboundLocalError as e:
            print(e)
            print("Error: could net scrape F1 data properly, aborting...")

html_boilerplate = "<!DOCTYPE html><html><body></body></html>"

def write_scraped_data(html_file: str, html_source: str):
    # Insert the two new HTML tables inside scraped_data.HTML
    with open(html_file, "w", encoding="UTF-8") as file:
        file.write(html_boilerplate)
        wrtite_pos = html_boilerplate.find("</body>")
        file.write(html_boilerplate[:wrtite_pos])
        file.write(html_source)
        file.write(html_boilerplate[wrtite_pos:])
        
scrape_pcs()
scrape_gprs()