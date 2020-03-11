from sys import path
path.insert(0, "../Interface")
from positions_sym import positions

positions_maxs = ['crunched', 'extended']

crunched = positions['crunched']
extended = positions['extended']

max_dict = {}
min_dict = {}

for key in crunched:
    if crunched[key] < extended[key]:
        max_dict[key] = extended[key]
        min_dict[key] = crunched[key]
    elif crunched[key] >= extended[key]:
        min_dict[key] = extended[key]
        max_dict[key] = crunched[key]

print max_dict
