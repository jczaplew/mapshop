import csv
import json
import urllib
import time

# Create a hash/dictionary to lookup restaurants
restauarant_lookup = {}

# Open the CSV files
with open("most_recent_food_scores.csv", "rb") as restaurants:
  # Create an object to read the file
  reader = csv.reader(restaurants)
  # Create and open the output file
  with open("most_recent_food_scores_geocoded.csv", "wb") as restaurants_out:
    # Create a writing object
    writer = csv.writer(restaurants_out)
    for i, row in enumerate(reader):
      if row[0] not in restauarant_lookup and i > 0:
        # Small time out to make sure we don't exceed our API request limit
        time.sleep(0.5)

        geocoded = json.loads(urllib.urlopen('https://maps.googleapis.com/maps/api/geocode/json?address=' + urllib.quote(row[2]) + ',Lexington%20KY').read())

        if len(geocoded["results"]) > 0: 
          restauarant_lookup[row[0]] = {"lat": geocoded["results"][0]["geometry"]["location"]["lat"], "lng": geocoded["results"][0]["geometry"]["location"]["lng"]}
        else: 
          restauarant_lookup[row[0]] = {"lat": "", "lng": ""}
          
        print row[1]

      else:
        # If it's the first row, write the header row
        if i == 0:
          writer.writerow((row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], "lat", "lng"))
        # Otherwise write a new row
        else:
          writer.writerow((row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], restauarant_lookup[row[0]]["lat"], restauarant_lookup[row[0]]["lng"]))
