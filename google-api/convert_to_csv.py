"""
Converts json file to csv. Need to flatten json first and remove nested objects
"""
import pandas as pd

json_file_name = "short.json"
with open(json_file_name, encoding='utf-8') as inputfile:
    df = pd.read_json(inputfile)

csv_file_name = 'csvfile.csv'
df.to_csv(csv_file_name, encoding='utf-8', index=False)
