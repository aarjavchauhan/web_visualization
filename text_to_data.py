import sys
import json

file = open(sys.argv[1], 'r')
lines = file.readlines()
output_file = sys.argv[1].replace(".txt", ".json")

obj = []

for line in lines:
    obj.append({ "url": line })

with open(output_file, 'w') as f:
     json.dump(obj, f)
