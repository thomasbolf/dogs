import os
import requests
import csv
from dotenv import load_dotenv
import json

load_dotenv()
API_KEY = os.getenv("API_KEY")
API_ENDPOINT = "https://api.petfinder.com/v2/animals"  # Replace with your API endpoint

HEADERS = {

    'Authorization': f'Bearer {API_KEY}'

}

def initialize_csv_files():
    with open("animals.csv", mode="w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "id", "organization_id",  "type", "species", "breed_primary", "breed_secondary",
            "is_mixed", "color_primary", "color_secondary", "color_tertiary", "age", "gender",
            "size", "coat", "name", "status", "spayed_neutered", "house_trained",
            "declawed", "special_needs", "shots_current", "children_friendly", "dogs_friendly",
            "cats_friendly", "email", "phone", "city", "state", "postcode", "county", "country", "published_at",
            "distance"
        ])

    with open("animal_tags.csv", mode="w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["animal_id", "tag"])
    
    with open("animal_photos.csv", mode="w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["animal_id", "photo_url", "size"])

    with open("animal_videos.csv", mode="w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["animal_id", "video_embed"])
with open('zips_to_fips.json') as f:
    zip_to_fips = json.load(f)

def map_zip_to_fips(zip_code):
    return zip_to_fips.get(zip_code, None) 

def write_animals_data(data):
        with open("animals.csv", mode="a", newline='', encoding="utf-8") as animals_file:
            animals_writer = csv.writer(animals_file)
            for animal in data["animals"]:
                animals_writer.writerow([
                    animal["id"],
                    animal["organization_id"],
                    animal["type"],
                    animal["species"],
                    animal["breeds"]["primary"],
                    animal["breeds"]["secondary"],
                    animal["breeds"]["mixed"],
                    animal["colors"]["primary"],
                    animal["colors"]["secondary"],
                    animal["colors"]["tertiary"],
                    animal["age"],
                    animal["gender"],
                    animal["size"],
                    animal["coat"],
                    animal["name"],
                    animal["status"],
                    animal["attributes"]["spayed_neutered"],
                    animal["attributes"]["house_trained"],
                    animal["attributes"]["declawed"],
                    animal["attributes"]["special_needs"],
                    animal["attributes"]["shots_current"],
                    animal["environment"]["children"],
                    animal["environment"]["dogs"],
                    animal["environment"]["cats"],
                    animal["contact"]["email"],
                    animal["contact"]["phone"],
                    animal["contact"]["address"]["city"],
                    animal["contact"]["address"]["state"],
                    animal["contact"]["address"]["postcode"],
                    map_zip_to_fips(animal["contact"]["address"]["postcode"]),
                    animal["contact"]["address"]["country"],
                    animal["published_at"],
                    animal["distance"]
                ])
        
# Write data to CSV files
def write_animal_data(data):
    with open("animals.csv", mode="a", newline='', encoding="utf-8") as animals_file, \
         open("animal_tags.csv", mode="a", newline='', encoding="utf-8") as tags_file, \
         open("animal_photos.csv", mode="a", newline='', encoding="utf-8") as photos_file, \
         open("animal_videos.csv", mode="a", newline='', encoding="utf-8") as videos_file:

        animals_writer = csv.writer(animals_file)
        tags_writer = csv.writer(tags_file)
        photos_writer = csv.writer(photos_file)
        videos_writer = csv.writer(videos_file)

        for animal in data["animals"]:
            # Write main animal data
            animals_writer.writerow([
                animal["id"],
                animal["organization_id"],
                animal["url"],
                animal["type"],
                animal["species"],
                animal["breeds"]["primary"],
                animal["breeds"]["secondary"],
                animal["breeds"]["mixed"],
                animal["colors"]["primary"],
                animal["colors"]["secondary"],
                animal["colors"]["tertiary"],
                animal["age"],
                animal["gender"],
                animal["size"],
                animal["coat"],
                animal["name"],
                animal["description"],
                animal["status"],
                animal["attributes"]["spayed_neutered"],
                animal["attributes"]["house_trained"],
                animal["attributes"]["declawed"],
                animal["attributes"]["special_needs"],
                animal["attributes"]["shots_current"],
                animal["environment"]["children"],
                animal["environment"]["dogs"],
                animal["environment"]["cats"],
                animal["contact"]["email"],
                animal["contact"]["phone"],
                animal["contact"]["address"]["city"],
                animal["contact"]["address"]["state"],
                animal["contact"]["address"]["postcode"],
                animal["contact"]["address"]["country"],
                animal["published_at"],
                animal["distance"]
            ])

            # Write tags
            for tag in animal.get("tags", []):
                tags_writer.writerow([animal["id"], tag])
            
            # Write photos
            for photo in animal.get("photos", []):
                for size, url in photo.items():
                    photos_writer.writerow([animal["id"], url, size])
            
            # Write videos
            for video in animal.get("videos", []):
                videos_writer.writerow([animal["id"], video["embed"]])


def fetch_and_store_data(page=1):
    params = {
        "page": page,
        "limit": 100, 
        "location": "TX",
        "distance": 480
    }
    response = requests.get(API_ENDPOINT, headers=HEADERS, params=params)

    if response.status_code == 200:
        data = response.json()
        write_animals_data(data)
        print(f"Page {page} processed.")
    else:
        print(f"Failed to fetch data for page {page}: {response.status_code}")

def main():
    initialize_csv_files()
    for i in range(1, 100): 
        fetch_and_store_data(page=i)

if __name__ == "__main__":
    main()
