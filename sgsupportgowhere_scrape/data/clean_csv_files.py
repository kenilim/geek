import pandas as pd
import os
import re

# Define the directory
directory = '/Users/kenilim/geek/sgsupportgowhere_scrape/data'

# Function to clean text by removing special characters except emails
def clean_text(text):
    email_regex = r'\S+@\S+'
    emails = re.findall(email_regex, text)
    text = re.sub(r'[^A-Za-z0-9\s@.]+', '', text)
    for email in emails:
        text = text.replace(email.replace('.', ''), email)
    return text

# Function to process each CSV file
def process_csv_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)
            print(f"Processing {file_path}...")
            try:
                df = pd.read_csv(file_path, delimiter=',')
                df = df.applymap(lambda x: clean_text(str(x)) if isinstance(x, str) else x)
                output_file_path = os.path.join(directory, f"Cleaned_{filename}")
                df.to_csv(output_file_path, index=False, sep=';')
                print(f"Cleaned file saved to: {output_file_path}")
            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")

# Process all CSV files in the directory
process_csv_files(directory)
