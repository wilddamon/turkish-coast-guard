import scrape

from datetime import datetime
import json
import os
import pandas

data = pandas.read_csv("../results/urls.csv")
data.set_index(data.columns[0], inplace=True)
for idx in data.index:
    if data.at[idx, "missing"]:
        print(idx)
        d = datetime.strptime(idx, "%Y-%m-%d").date()

        datestr = f"{d.day:02}-{d.day+2:02}-{d.strftime('%B-%Y')}".lower()
        if os.path.exists(f"../results/queries/{datestr}.txt") or os.path.exists(f"../results/results/{datestr}.json"):
            continue

        with open(f"../results/queries/{datestr}.txt", "w") as f:
            f.write(datestr)

        url = f"https://en.sg.gov.tr/current-operations-{datestr}"

        print(url)
        r = scrape.scrape_url(datestr, url)

        if r is None:
            url = f"https://en.sg.gov.tr/current-operation-{datestr}"
            print(url)
            r = scrape.scrape_url(datestr, url)


        if r is not None:
            with open(f"../results/results/{datestr}.json", "w") as f:
                json.dump(r, f, indent=4)
