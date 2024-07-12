import csv
import os
import argparse
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import re
import pytz


def convert_to_unix_timestamp(date_str):
    """Konvertiere ein Datum im Format 'YYYY-MM-DD' in einen Unix-Timestamp in Millisekunden unter Verwendung von UTC."""
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    utc_dt = dt.replace(tzinfo=pytz.UTC)
    timestamp = int(utc_dt.timestamp() * 1000)
    return timestamp


def create_url(start_date, end_date):
    """Erstelle die URL mit den angegebenen Start- und Enddaten."""
    start_timestamp = convert_to_unix_timestamp(start_date)
    end_timestamp = convert_to_unix_timestamp(end_date)

    url_template = (
        "https://www.melia.com/de/booking?search=%7B%22destination%22%3A%7B%22id%22%3A%226595%22%2C%22hotel%22%3A%22Meli%C3%A1+Frankfurt+City%22%2C%22city%22%3A%22Frankfurt%22%2C%22country%22%3A%22Deutschland%22%7D%2C%22occupation%22%3A%5B%7B%22adults%22%3A2%2C%22childrenAges%22%3A%5B%5D%7D%5D%2C%22calendar%22%3A%7B%22dates%22%3A%5B{start_timestamp}%2C{end_timestamp}%5D%2C%22locale%22%3A%22de%22%7D%2C%22hotels%22%3A%5B%226595%22%5D%7D"
    )
    url = url_template.format(start_timestamp=start_timestamp, end_timestamp=end_timestamp)
    return url


def fetch_page_content_with_js(url, output_file, date_range, csv_writer):
    """Rufe den Inhalt der Webseite ab, führe die JavaScript-Skripte aus und speichere den finalen Quellcode in einer Datei."""
    # Set up Selenium with Chrome WebDriver
    options = Options()
    options.headless = True  # Headless mode, damit kein Browserfenster geöffnet wird
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Rufe die Webseite auf
    driver.get(url)

    # Warte einige Sekunden, um sicherzustellen, dass alle Skripte ausgeführt werden
    time.sleep(10)

    # Holen Sie den endgültigen Quellcode der Seite
    page_source = driver.page_source

    # Schließe den WebDriver
    driver.quit()

    # Speichere den Quellcode in einer Datei
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(page_source)

    # Suche nach span-Elementen mit den Titeln, die auf "-C2T-C2A", "-SJS-SJA", und "-E2T-E2D" enden
    soup = BeautifulSoup(page_source, 'html.parser')

    # Bereite Daten für die CSV-Datei vor
    row = [date_range]

    # Suche nach Titeln, die auf "-C2T-C2A" enden
    melia_zimmer = ""
    span_elements_c2t_c2a = soup.find_all('span', title=re.compile(r'-C2T-C2A$'))
    for span in span_elements_c2t_c2a:
        strong = span.find('strong')
        if strong:
            melia_zimmer = strong.text.replace('\xa0', ' ')
    row.append(melia_zimmer)

    # Suche nach Titeln, die auf "-SJS-SJA" enden
    junior_suite = ""
    span_elements_sjs_sja = soup.find_all('span', title=re.compile(r'-SJS-SJA$'))
    for span in span_elements_sjs_sja:
        strong = span.find('strong')
        if strong:
            junior_suite = strong.text.replace('\xa0', ' ')
    row.append(junior_suite)

    # Suche nach Titeln, die auf "-E2T-E2D" enden
    the_level_zimmer = ""
    span_elements_e2t_e2d = soup.find_all('span', title=re.compile(r'-E2T-E2D$'))
    for span in span_elements_e2t_e2d:
        strong = span.find('strong')
        if strong:
            the_level_zimmer = strong.text.replace('\xa0', ' ')
    row.append(the_level_zimmer)

    # Schreibe die Zeile in die CSV-Datei
    csv_writer.writerow(row)

    # Konsole Ausgabe
    print(f"Ergebnisse für den Zeitraum: {date_range}")
    print(f"Melia Zimmer: {melia_zimmer}")
    print(f"Junior Suite: {junior_suite}")
    print(f"The Level Zimmer: {the_level_zimmer}")

    # Lösche die HTML-Datei
    os.remove(output_file)


def main(start_date, end_date):
    """Hauptfunktion, die das Skript steuert."""
    current_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")

    csv_file = "buchungsanfragen.csv"
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        # Schreibe die Kopfzeile in die CSV-Datei
        csv_writer.writerow(["Zeitraum", "Melia Zimmer", "Junior Suite", "The Level Zimmer"])

        while current_date < end_date_dt:
            next_date = current_date + timedelta(days=1)
            date_range = f"{current_date.strftime('%Y-%m-%d')} bis {next_date.strftime('%Y-%m-%d')}"
            url = create_url(current_date.strftime('%Y-%m-%d'), next_date.strftime('%Y-%m-%d'))
            output_file = f"webpage_final_source_{current_date.strftime('%Y-%m-%d')}.html"
            fetch_page_content_with_js(url, output_file, date_range, csv_writer)
            current_date = next_date


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape data from Meliá hotel booking site.")
    parser.add_argument("-s", "--start", dest="start_date", required=True,
                        help="Start date for scraping in format 'YYYY-MM-DD'")
    parser.add_argument("-e", "--end", dest="end_date", required=True,
                        help="End date for scraping in format 'YYYY-MM-DD'")
    args = parser.parse_args()

    main(args.start_date, args.end_date)
