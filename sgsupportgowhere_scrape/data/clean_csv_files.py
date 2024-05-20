import os
import pandas as pd
import re

def clean_text(text):
    if isinstance(text, str):
        # Remove special characters except for emails
        text = re.sub(r'[^a-zA-Z0-9\s@.-]', ' ', text)
    return text

def process_csv_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            filepath = os.path.join(directory, filename)
            print(f"Processing {filepath}...")

            df = pd.read_csv(filepath, delimiter=',')
            df = df.applymap(clean_text)

            # Write the cleaned data back to the file
            df.to_csv(filepath, index=False, sep=';')
            print(f"Finished processing {filepath}")

directory = "/Users/kenilim/geek/sgsupportgowhere_scrape/data/"
process_csv_files(directory)
