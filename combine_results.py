import collections
from datetime import datetime,date, timedelta
import json
import os
import pandas


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



result = collections.defaultdict(list)

dirname = "../results/results/"
fnames = os.listdir(dirname)
fnames = sorted(fnames)
for fname in fnames:
    if not fname.endswith("json"):
        continue

    date_str = fname.split(".")[0]
    date_parts = date_str.split("-")
    d = datetime.strptime(f"{date_parts[0]} {date_parts[-2]} {date_parts[-1]}", "%d %B %Y").date()

    print(fname)
    with open(dirname + fname, 'r') as f:
        j = json.load(f)

    update_result(d, f"\"{date_str}\"", j, result)

df = pandas.DataFrame(result)
df.set_index("date", inplace=True)
df["missing"] = False

# Find missing dates
missing = []
startdate = date(2020, 8, 1)
enddate = date.today()
d = startdate
while d < enddate:
    if d not in df.index:
        missing.append(d)
    d += timedelta(days=1)
empty_df = pandas.DataFrame(index=missing, columns=df.columns)
empty_df["missing"] = True
df = pandas.concat([df, empty_df])

df.sort_index(inplace=True)
df.to_csv("../results/urls.csv")
