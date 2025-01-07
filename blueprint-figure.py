import base64
import json
import zlib
from PIL import Image

filename = "lamp3.txt"
blueprint_file = "anon.txt"

substatio_range = 18
substatio_position = substatio_range // 2
space_list = [substatio_range // 2, substatio_range // 2 - 1]


im = Image.open('anon-150.jpg')
pix = im.load()

image_pixel = im.size[0]

substatio_num = (image_pixel + 8) // substatio_range


f = open(filename, 'r')
s = f.read()
s1= base64.b64decode(s[1:])
s2= zlib.decompress(s1).decode('utf8')
j = json.loads(s2)

j["blueprint"]['snap-to-grid']['x'] = j["blueprint"]['snap-to-grid']['y'] = image_pixel

entity_number = 0

for y in range(image_pixel):
  for x in range(image_pixel):
    if x%substatio_range == substatio_position and y%substatio_range == substatio_position:
      j["blueprint"]["entities"].append({'entity_number': entity_number, 'name': 'substation', 'position': {'x': x, 'y': y}})
      entity_number += 1

for y in range(image_pixel):
  for x in range(image_pixel):
    if x%substatio_range in space_list and y%substatio_range in space_list:
      continue

    now_px = pix[x,y]
    j["blueprint"]["entities"].append({'entity_number': entity_number, 'name': 'small-lamp', 'position': {'x': x + 0.5, 'y': y + 0.5}, 'color': {'r': now_px[0] / 255, 'g': now_px[1] / 255, 'b': now_px[2] / 255, 'a': 1}, 'always_on': True})

    entity_number += 1

wires = []
for ii in range(substatio_num):
  for jj in range(substatio_num-1):
    wires.append([ii*substatio_num + jj, 5, ii*substatio_num + jj + 1, 5])


j["blueprint"]['wires'] = wires
# j["blueprint"]['wires'].entend(wires)


del j["blueprint"]["entities"][0]
del j["blueprint"]["entities"][0]
del j["blueprint"]["entities"][0]


s3 = json.dumps(j)
s4 = zlib.compress(s3.encode())
s5 = str(base64.b64encode(s4), 'utf-8')

with open(blueprint_file, 'w') as b:
  b.write('0')
  b.write(s5)
