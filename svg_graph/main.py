# -*- mode: python; coding utf-8 -*-

import xml.etree.ElementTree as ET


class LineGraph(object):

    def __init__(self, title, hight, width, points, labels):
        self.title = title
        self.hight = hight
        self.width = width
        self.labels = labels

        self.points = points
        self.over = 100

    def get_label_positions(self, axis):
        if axis == 'x':
            labels = self.labels[0][1]
            total = self.width
        else:
            labels = list(reversed(self.labels[1][1]))
            total = self.hight

        interlabel_distance = total / (len(labels) - 1)
        for i, label in enumerate(labels):
            if label is None:
                continue
            yield str(int(i * interlabel_distance)), str(label)

    def __str__(self):

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
                                    'transform': 'translate(%(over)s,0)' % dict(over=self.over)})
        line_x = ET.Element(
            'line',
            attrib={
                'x1': '0',
                'y1': '0',
                'x2': '0',
                'y2': str(self.hight),
            },
        )
        g.append(line_x)
        svg.append(g)

        g = ET.Element('g', attrib={'class': 'grid y-grid', 'id': 'yGrid',
                                    'transform': 'translate(%(over)s,0)' % dict(over=self.over)})
        line_y = ET.Element(
            'line',
            attrib={
                'x1': '0',
                'y1': str(self.hight),
                'x2': str(self.width),
                'y2': str(self.hight),
            },
        )
        g.append(line_y)
        svg.append(g)

        g = ET.Element('g', attrib={
            'class': 'labels x-labels',
            'transform': 'translate(%(over)s,20)' % dict(over=self.over)})
        for x, label in self.get_label_positions('x'):
            text = ET.Element('text', attrib={'x': x, 'y': str(self.hight)})
            text.text = label
            g.append(text)
        text = ET.Element('text', attrib={
            'x': str(int(self.width / 2)),
            'y': str(int(self.hight + 40)),
            'class': 'label-title'})
        text.text = self.labels[0][0]
        g.append(text)
        svg.append(g)

        g = ET.Element('g', attrib={'class': 'labels y-labels'})
        for y, label in self.get_label_positions('y'):
            text = ET.Element('text', attrib={'x': str(self.over - 20), 'y': y})
            text.text = label
            g.append(text)
        text = ET.Element('text', attrib={
            'x': str(self.over / 2),
            'y': str(self.hight / 2),
            'class': 'label-title'})
        text.text = self.labels[1][0]
        g.append(text)
        svg.append(g)

        points = []
        for x, y in self.points:
            h = x
            v = self.hight - y
            points.append('%s, %s' % (h, v))
        points = '\n'.join(points)
        points = '\n' + points + '\n'
        g = ET.Element('g', attrib={'transform': 'translate(%(over)s,0)' % dict(over=self.over)})
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

    import webbrowser
    import pathlib
    import os

    from tests import top, bottom

    lg = LineGraph('Look at This Graph',
                   hight=400,
                   width=700,
                   points=[
                       (0,0),
                       (2, 3),
                       (53, 87),
                       (99, 200),
                       (444, 50),
                       (600,300)],
                   labels=[
                       ('Year', (2008, 2009, 2010, 2011, 2012)),
                       ('Price', (None, 5, 10, 14))]
    )

    page = top + str(lg) + bottom
    # Yuck. Don't know how to get around using a file.
    path = '/tmp/.test.html'
    with open(path, 'w') as f:
        f.write(page)

    uri = pathlib.Path(path).as_uri()

    webbrowser.open(uri, new=0, autoraise=True)
