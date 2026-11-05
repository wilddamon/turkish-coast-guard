import collections
from datetime import datetime, date
from docx import Document
import locale
import os
import pandas
import re
from unidecode import unidecode

from country_aliases import unalias_country, unalias_province, unalias_district


data_names = [
    "nu",
    "date",
    "location",
    "asset",
    "num_facilitators",
    "total_rescued",
    "nationalities",
]


def try_parse_date(s):
    try:
        return datetime.strptime(s, "%d %B %Y").date()
    except ValueError:
        pass

    locale.setlocale(locale.LC_ALL, "tr_TR.UTF-8")
    try:
        return datetime.strptime(s, "%d %B %Y").date()
    except ValueError:
        pass
    finally:
        locale.setlocale(locale.LC_ALL, "")

    if s == "14 May 23":
        return date(2023, 5, 14)
    if s == "04 December2021":
        return date(2021, 12, 4)

    print(s)
    return s


def get_num_rescued(path_to_file):
    doc = Document(path_to_file)

    result = collections.defaultdict(list)
    for table in doc.tables:

        # ignore title row
        for i in range(1, len(table.rows)):
            result["nu"].append(unidecode(table.rows[i].cells[0].text).strip())
            # handle date separately
            result["date"].append(try_parse_date(table.rows[i].cells[1].text.strip()))
            for j in range(2, len(data_names)):
                result[data_names[j]].append(unidecode(table.rows[i].cells[j].text).strip())

    return result


def extract_time(s):
    pt = s.split(" ")[-1]
    if re.search(r"^\d{2}\.\d{2}$", pt):
        return pt
    if s == "CANAKKALE/Ayvaci06.50":
        return "06.50"
    return None


def extract_province(s):
    match = re.search(r"\b(\w+)\/", s)
    if match:
        return unalias_province(match.group(1).lower())
    return None


def extract_district(s):
    match = re.search(r"\/([a-zA-Zi ]+)", s)
    if match:
        return unalias_district(match.group(1).lower().strip())
    return None


dirname = "../results/rescued_docx/"
fnames = os.listdir(dirname)
print(f"Found {len(fnames)} files")
result = collections.defaultdict(list)
for fname in fnames:
    if not fname.endswith("docx"):
        continue
    new_data = get_num_rescued(dirname + fname)

    # This one seems to have the numbers in the wrong columns
    if fname == "14-15-march-2022.docx":
        f = new_data["total_rescued"]
        new_data["total_rescued"] = new_data["num_facilitators"]
        new_data["num_facilitators"] = f

    for i in range(len(data_names)):
        result[data_names[i]] += new_data[data_names[i]]

df = pandas.DataFrame(data=result)

# Constrain dates
startdate = date(2021, 1, 1)
enddate = date(2025, 12, 31)
df = df[(df["date"] >= startdate) & (df["date"] <= enddate)]

# Process columns
df["location"] = df["location"].replace(r"\s", " ", regex=True)
df["time"] = df["location"].apply(extract_time)
df["province"] = df["location"].apply(extract_province)
df["district"] = df["location"].apply(extract_district)
with pandas.option_context("display.max_rows", None):
    print(df["province"].value_counts(dropna=False))
with pandas.option_context("display.max_rows", None):
    print(df["district"].value_counts(dropna=False))


nationalities = []


def add_nationality(idx, s):
    pat = r"(-?\d+) ?((?:[a-z_]+ ?)+)"
    s = re.sub(r"\s+", " ", s.strip()).lower()
    # Remove "."s.
    s = re.sub(r"\.", "", s)
    match = re.search(pat, s)
    while match:
        if (
            "child" in match.group(2)
            or "chilren" in match.group(2)
            or "dead" in match.group(2)
            or "deceased" in match.group(2)
            or "irregular" in match.group(2)
        ):
            # Discard until next ")"
            s = s[match.end() :]
            bracket = s.find(")")
            if bracket == -1:
                break
            s = s[bracket + 1 :]
            match = re.search(pat, s)
            continue

        nationality = unalias_country(match.group(2).strip())
        if nationality not in df.columns:
            df[nationality] = None
            nationalities.append(nationality)

        num = int(match.group(1))
        if num > 0:
            if pandas.isna(df.at[idx, nationality]):
                df.at[idx, nationality] = 0
            df.at[idx, nationality] += int(match.group(1))

        s = s[match.end() :]
        match = re.search(pat, s)


# Do nationality columns
df["unknown_nationality"] = None
for idx in df.index:
    s = df.at[idx, "nationalities"]
    if pandas.isna(s) or s == "-":
        continue

    if df.at[idx, "date"] == date(2020, 9, 8) and df.at[idx, "nu"] == "3":
        df.at[idx, "total_rescued"] = 13
        add_nationality(idx, s)
    elif df.at[idx, "date"] == date(2022, 8, 5) and df.at[idx, "nu"] == "1":
        df.at[idx, "yemen"] = 25
        df.at[idx, "eritrea"] = 9
        df.at[idx, "mali"] = 1
    elif df.at[idx, "date"] == date(2023, 12, 24) and df.at[idx, "nu"] == "1":
        df.at[idx, "total_rescued"] = 22
        add_nationality(idx, s)
    elif df.at[idx, "date"] == date(2024, 2, 3) and df.at[idx, "nu"] == "2":
        df.at[idx, "afghanistan"] = 51
    elif df.at[idx, "date"] == date(2024, 2, 24) and df.at[idx, "nu"] == "1":
        df.at[idx, "total_rescued"] = 24
        add_nationality(idx, s)
    elif df.at[idx, "date"] == date(2024, 2, 29) and df.at[idx, "nu"] == "2":
        df.at[idx, "afghanistan"] = 36
        df.at[idx, "iran"] = 2
    elif df.at[idx, "date"] == date(2024, 10, 25) and df.at[idx, "nu"] == "1":
        df.at[idx, "total_rescued"] = 44
        add_nationality(idx, s)
    else:
        add_nationality(idx, s)

    # Add up nationality columns, add "unkonwn"
    if df.at[idx, "total_rescued"] == "-":
        continue

    known_nationalities = 0
    for nationality in nationalities:
        if nationality == "turkiye":
            continue
        if pandas.notna(df.at[idx, nationality]):
            known_nationalities += int(df.at[idx, nationality])
    num_unknown = int(df.at[idx, "total_rescued"]) - known_nationalities
    add_nationality(idx, f"{num_unknown} unknown_nationality")


# construct total counts
nationality_counts = {"name": [], "counts": []}
for nationality in nationalities:
    nationality_counts["name"].append(nationality)
    nationality_counts["counts"].append(df[nationality].sum())
with pandas.option_context("display.max_rows", None):
    print(pandas.DataFrame(nationality_counts).sort_values("counts", ascending=False))


# Look for children
def extract_children(s):
    s = s.lower()
    s = re.sub(r"\s+", " ", s)
    child_match = re.search(r"(\d+) ?of them child?(?:ren)?", s)
    if child_match:
        return int(child_match.group(1))

    child_match = re.search(r"\((\d+).si cocuk\)", s)
    if child_match:
        return int(child_match.group(1))


df["num_children"] = df["nationalities"].apply(extract_children)
print(f'num_children: {df["num_children"].sum()}')

# Look for deceased
def extract_num_deceased(s):
    match = re.search(
        r"(?:(\d+)|(\d+)) ?\(? ?(?:dead|deceased) bod(?:y|ies)", s.lower()
    )

    if match:
        for g in match.groups():
            if g is not None:
                return int(g)
    return None


df["num_deceased"] = df["nationalities"].apply(extract_num_deceased)
print(f'num_deceased: {df["num_deceased"].sum()}')

df.sort_values("date", inplace=True)
# Redo the index to ascending values based on the new order.
df.index = range(len(df))

# Re-order columns
district_idx = df.columns.get_loc("district")
nationalities = sorted(nationalities)
col_order = (
    df.columns[1: district_idx + 1].to_list()
    + nationalities
    + ["unknown_nationality", "num_children", "num_deceased"]
)
df = df[col_order]

df.to_csv("../results/extracted.csv")
