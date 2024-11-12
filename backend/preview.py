import csv
import pandas as pd

df = pd.read_csv('animals.csv')

county_counts = df['county'].value_counts().reset_index()
county_counts.columns = ['county', 'frequency']
##add a column that uses fips_to_county.csv to add a county column
fips_to_county = pd.read_csv('fips_to_county.csv')
county_counts = pd.merge(county_counts, fips_to_county, on='county', how='left')
print(county_counts)
county_counts.drop("lng", axis=1).drop("lat", axis=1).to_csv('county_counts.csv', index=False)
#count the number of unique organization_id for state==Texas
texas_org_id_counts = df[df['state'] == 'TX']['organization_id'].nunique()
#count the number of unique id for state==Texas
texas_id_counts = df[df['state'] == 'TX']['id'].nunique()
print(texas_org_id_counts)
print(texas_id_counts)
#give me top 10 most frequent breed_primary
top_10_breed_primary = df['breed_primary'].value_counts().head(10)
print(top_10_breed_primary)
#count number of breed_secondary 
breed_secondary_counts = df['breed_secondary'].value_counts().head(10)  
print(breed_secondary_counts)