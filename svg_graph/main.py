import xml.etree.ElementTree as ET

top = """<html>
    <head>
	<style>
	 body {
	     font-family: 'Open Sans', sans-serif;
	 }

	 .graph .labels.x-labels {
	     text-anchor: middle;
	 }

	 .graph .labels.y-labels {
	     text-anchor: end;
	 }


	 .graph {
	     height: 500px;
	     width: 800px;
	 }

	 .graph .grid {
	     stroke: #ccc;
	     stroke-dasharray: 0;
	     stroke-width: 1;
	 }

	 .labels {
	     font-size: 13px;
	 }

	 .label-title {
	     font-weight: bold;
	     text-transform: uppercase;
	     font-size: 12px;
	     fill: black;
	 }

	 .data {
	     fill: red;
	     stroke-width: 1;
	</style>
    </head>
    <body>
"""

bottom = """    </body>
</html>"""

class LineGraph(object):

    def __init__(self, title, origin, hight, width, points):
        self.title = title
        self.origin = origin  # 0/400
        self.hight = hight
        self.width = width

        self.points = points

        self.left = self.origin[0]
        self.bottom = self.hight
        self.right = self.width
        self.top = self.origin[1] - self.hight

    def __getattr__(self, name):
        if not name.startswith('str_'):
            raise AttributeError(name)
        real_name = name[4:]
        return str(getattr(self, real_name))

    def __str__(self):

        over = '100'

        svg = ET.Element(
            'svg',
            attrib={
                'version': '1.2',
                'xmlns': 'http://www.w3.org/2000/svg',
                'xmlns:xlink': 'http://www.w3.org/1999/xlink',
                'class': 'graph',
                'aria-labelledby': 'title',
                'role': 'img',
            }
        )

        title = ET.Element('title', attib={'id': 'title'})
        title.text = self.title

        g = ET.Element('g', attrib={'class': 'grid x-grid', 'id': 'xGrid',
                                    'transform': 'translate(%(over)s,0)' % dict(over=over)})
        line_x = ET.Element(
            'line',
            attrib={
                'x1': self.str_left,
                'y1': self.str_top,
                'x2': self.str_left,
                'y2': self.str_bottom,
            },
        )
        g.append(line_x)
        svg.append(g)

        g = ET.Element('g', attrib={'class': 'grid y-grid', 'id': 'yGrid',
                                    'transform': 'translate(%(over)s,0)' % dict(over=over)})
        line_y = ET.Element(
            'line',
            attrib={
                'x1': self.str_left,
                'y1': self.str_bottom,
                'x2': self.str_right,
                'y2': self.str_bottom,
            },
        )
        g.append(line_y)
        svg.append(g)

        g = ET.Element('g', attrib={'class': 'labels x-labels',
                                    'transform': 'translate(%(over)s,20)' % dict(over=over)})
        for x, label in [
                ('100', '2008'),
                ('246', '2009'),
                ('392', '2010'),
                ('538', '2011'),
                ('684', '2012'),]:
            text = ET.Element('text', attrib={'x': x, 'y': '400'})
            text.text = label
            g.append(text)
        text = ET.Element('text', attrib={'x': '400', 'y': '440', 'class': 'label-title'})
        text.text = 'Year'
        g.append(text)
        svg.append(g)

        g = ET.Element('g', attrib={'class': 'labels y-labels'})
        for y, label in [
                ('15', '15'),
                ('131', '10'),
                ('248', '5'),
                ('373', '0'),]:
            text = ET.Element('text', attrib={'x': '80', 'y': y})
            text.text = label
            g.append(text)
        text = ET.Element('text', attrib={'x': '50', 'y': '200', 'class': 'Price'})
        text.text = 'Year'
        g.append(text)
        svg.append(g)

        points = []
        for x, y in self.points:
            h = x
            v = self.hight - y
            points.append('%s, %s' % (h, v))
        points = '\n'.join(points)
        points = '\n' + points + '\n'
        g = ET.Element('g', attrib={'transform': 'translate(%(over)s,0)' % dict(over=over)})
        polyline = ET.Element(
            'polyline',
            attrib={
                'fill': 'none',
                'stroke': '#0074d9',
                'stroke-width': '2',
                'points': points,
            },
        )
        g.append(polyline)
        svg.append(g)
        fix_encoding = ET.tostring(svg).decode('utf-8')
        return fix_encoding.replace('&#10;', '\n')  # ZMG FIXME ZZZ TODO

if __name__ == '__main__':

    lg = LineGraph('Look at This Graph', (0, 400),
                   hight=400,
                   width=700,
                   points=[
                       (0,0),
                       (2, 3),
                       (53, 87),
                       (99, 200),
                       (444, 50),
                       (600,300),
                   ])

    print(top, lg, bottom)
