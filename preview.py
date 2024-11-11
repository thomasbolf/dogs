import csv
import pandas as pd

df = pd.read_csv('animals.csv')

county_counts = df['county'].value_counts().reset_index()
county_counts.columns = ['county', 'frequency']

print(county_counts)
county_counts.to_csv('county_counts.csv', index=False)