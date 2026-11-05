import os
import pandas
import requests


data = pandas.read_csv("../results/urls_annotated-2026-01-13T12-29.csv", encoding_errors='replace')
data.set_index(data.columns[0], inplace=True)
for idx in data.index:
    r_url = data.at[idx, "rescued_url"]
    print(f"URL for {idx}: {r_url}")
    if pandas.isna(r_url):
        continue

    date_str = data.at[idx, "datestr"]
    date_str = date_str.replace("\"", "")
    local_path = f"../results/rescued_docx/{date_str}.docx"

    if os.path.exists(local_path):
        continue

    print(r_url)
    try:
        response = requests.get(r_url, stream=True)
        response.raise_for_status()

        with open(local_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
