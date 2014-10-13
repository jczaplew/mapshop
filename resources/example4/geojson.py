import csv
import json

restaurant_hash = {}
feature_collection = {'type': 'FeatureCollection', 'features': []}

def get_inspection(row):
  violations_split = row[6].split("  ")
  violations = []
  for violation in violations:
    if len(violation) > 0:
      violations.append(int(violation))

  inspection = {
    'inspection_type': row[3],
    'score': int(row[4]),
    'date': row[5],
    'violations': violations,
    'followup': row[7]
  }
  return inspection

with open("restaurant_scores_geocoded.csv", "rb") as restaurants:
  reader = csv.reader(restaurants)
  for i, row in enumerate(reader):
    if row[0] not in restaurant_hash and i > 0:
      inspection = get_inspection(row)

      feature = {
        'type': 'Feature',
        'geometry': {'type':'Point','coordinates':[float(row[10]), float(row[9])]},
        'properties': {
          'id': row[0],
          'name': row[1],
          'address': row[2],
          'opened': row[8],
          'inspections': [ inspection ]
        }
      }

      restaurant_hash[row[0]] = feature

    elif i > 0: 
      inspection = get_inspection(row)
      restaurant_hash[row[0]]['properties']['inspections'].append(inspection)

  for key, value in restaurant_hash.iteritems():
    feature_collection['features'].append(value)

  #print feature_collection
  with open("restaurants.json", "w") as output_geojson:
    json.dump(feature_collection, output_geojson)
