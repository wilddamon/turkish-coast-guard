from urllib.request import urlopen
from datetime import date,timedelta
from bs4 import BeautifulSoup
import collections
import json
import os
import pandas
import sys


def scrape_url(datestr, url):
    try:
        with urlopen(url) as response:
            html_content = response.read().decode('utf-8')

        with open(f"../results/html-results/{datestr}.html", "w") as f:
            f.write(html_content)

        soup = BeautifulSoup(html_content, 'html.parser')

        result = {}
        for link in soup.find_all('a'):
            href = link.get('href')
            if href is not None and "docx" in href:
                outer = link.parent.parent
                text = outer.contents[1].contents[0]

                if href[:4] != "http":
                    href = "https://en.sg.gov.tr" + href

                if "rescued" in text:
                    result["rescued"] = (text, href)
                elif "apprehended" in text:
                    result["apprehended"] = (text, href)
                else:
                    result["unknown"] = (text, href)

        return result

    except Exception as e:
        print(e)
        return None


def update_result(date, datestr, r, result):
    result["date"].append(date)
    result["datestr"].append(datestr)

    def update_pair(name):
        if r is None or name not in r:
            result[name].append(None)
            result[f"{name}_url"].append(None)
        else:
            result[name].append(r[name][0])
            result[f"{name}_url"].append(r[name][1])

    update_pair("rescued")
    update_pair("apprehended")
    update_pair("unknown")


def scrape(startdate, enddate):
    d = startdate
    while d < enddate:
        datestr = d.strftime('%d-%B-%Y').lower()
        url = f"https://en.sg.gov.tr/current-operations-{datestr}"
        if os.path.exists(f"../results/queries/{datestr}.txt") or os.path.exists(f"../results/results/{datestr}.json"):
            d = d + timedelta(days=1)
            continue

        print(url)
        with open(f"../results/queries/{datestr}.txt", "w") as f:
            f.write(datestr)
        r = scrape_url(datestr, url)

        if r is None:
            # first try with "operation" instead of operations
            url = f"https://en.sg.gov.tr/current-operation-{datestr}"
            print(url)
            r = scrape_url(datestr, url)

        if r is None:
            datestr = f"{d.day:02}-{d.day+1:02}-{d.strftime('%B-%Y')}".lower()
            url = f"https://en.sg.gov.tr/current-operations-{datestr}"
            print(url)
            r = scrape_url(datestr, url)

        if r is None:
            url = f"https://en.sg.gov.tr/current-operation-{datestr}"
            print(url)
            r = scrape_url(datestr, url)

        if r is not None:
            with open(f"../results/results/{datestr}.json", "w") as f:
                json.dump(r, f, indent=4)

        d = d + timedelta(days=1)


def main():
    # startdate = date(2020, 8, 1)
    startdate = date(2021, 1, 1)
    enddate = date(2026, 1, 1)

    scrape(startdate, enddate)


if __name__ == "__main__":
    sys.exit(main())
