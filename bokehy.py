import json
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
from numpy import pi


#~ EXAMPLES ~#
'''
p = figure(x_range=(-1,10))
p.vbar(x=[0,1], top=[25,50], width=0.7)
show(p)

p2 = figure(x_range=(-10,10))
p2.wedge(x=0, y=0, radius=5,
         start_angle = [1/4*pi, 6/4*pi],
         end_angle = [6/4*pi, 1/4*pi],
         color = ["purple", "darkblue"])
show(p2)
'''

'''
src = ColumnDataSource(data = {
    'start': [1/4*pi, 6/4*pi],
    'end': [6/4*pi, 1/4*pi],
    'color': ["purple", "darkblue"],
    'label': ["mlem", "purr"]})

p = figure()
p.wedge(x=0, y=0, radius = 5,
        start_angle = 'start',
        end_angle = 'end',
        color = 'color',
        legend = 'label',
        source = src)
show(p)
'''

l = { 'shares': [],
      'colors': [],
      'labels': [] }

f = open('election.json', 'r')
#p = figure(x_range=(-1,20))
sum_below_1 = 0
for item in sorted(json.load(f), key=lambda x: -x['share']):
    if item['share'] <= 1:
        sum_below_1 += item['share']
    else:
        l['shares'].append(item['share'])
        if 'color' in item:
            l['colors'].append(item['color'])
        else:
            l['colors'].append('gray')
        if 'short' in item:
            l['labels'].append(item['short'])
        else:
            l['labels'].append(item['name'][0:10])
l['shares'].append(sum_below_1)
l['colors'].append('gray')
l['labels'].append("zvyšný bordel")

# BAR CHART #
'''
src = ColumnDataSource(data = {
    'x': range(len(l['shares'])),
    'color': l['colors'],
    'label': l['labels'],
    'top': l['shares'] })

p.vbar(x='x', top='top', width=0.7,
       color='color', legend='label', source=src)
show(p)
'''

# PIE CHART #
starts = []
ends = []

current = 0
for share in l['shares']:
    starts.append(current*2*pi/100)
    current += share
    ends.append(current*2*pi/100)
ends[-1] = 0

src = ColumnDataSource(data = {
    'start': starts,
    'end': ends,
    'color': l['colors'],
    'label': l['labels']})

p = figure(x_range=(-1,2))
p.wedge(x=None, y=None, radius = 1,
        start_angle = 'start',
        end_angle = 'end',
        color = 'color',
        legend = 'label',
        source = src,
        direction = 'anticlock')
# direction = 'clock', 'anticlock'

show(p)
