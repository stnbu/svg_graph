# -*- mode: python; coding utf-8 -*-

from xml.etree.ElementTree import Element, tostring


class LineGraph(object):

    def __init__(self, title, height, width, points, labels):

        self.title = title

        self.height = height
        self.width = width
        self.labels = labels
        self.points = points

        self.right = 100
        self.down = 0

    def get_label_positions(self, axis, labels_object):
        if axis == 'x':
            labels = labels_object.values
            total = self.width
        elif axis == 'y':
            labels = list(reversed(labels_object.values))
            total = self.height
        else:
            raise ValueError('do not understand axis="%s"' % axis)

        interlabel_distance = total / (len(labels) - 1)
        for i, label in enumerate(labels):
            if i == 0 and not labels_object.include_zeroith:
                continue
            yield str(int(i * interlabel_distance)), str(label)

    def __str__(self):

        style = Element('style')
        style.text = """
        /* requires HTML5.2 */
        /* https://www.w3.org/TR/html52/document-metadata.html#the-style-element */
        .main {
            transform: translate(%(right)spx, %(down)spx);
            /* height: %(height)spx;
            width: %(width)spx; */
        }
        .graph {
            height: %(height)spx;
            width: %(width)spx;
        }
        .axis {
            stroke: #ccc;
            stroke-dasharray: 0;
            stroke-width: 1;
        }
        .labels.x-labels {
            text-anchor: middle;
        }
        .labels.y-labels {
            text-anchor: end;
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
        """ % dict(
            right=self.right,
            down=self.down,
            height=self.height+self.down+100,
            width=self.width+self.right+100,
        )

        svg = Element(
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

        title = Element('title', attib={'id': 'title'})
        title.text = self.title

        g = Element('g', attrib={'class': 'axis main'})
        line_x = Element(
            'line',
            attrib={
                'x1': '0',
                'y1': '0',
                'x2': '0',
                'y2': str(self.height),
            },
        )
        g.append(line_x)
        svg.append(g)

        g = Element('g', attrib={'class': 'axis main'})
        line_y = Element(
            'line',
            attrib={
                'x1': '0',
                'y1': str(self.height),
                'x2': str(self.width),
                'y2': str(self.height),
            },
        )
        g.append(line_y)
        svg.append(g)

        #---
        g = Element('g', attrib={
            'class': 'labels x-labels',
            'transform': 'translate(%(right)s,20)' % dict(right=self.right)})
        for x, label in self.get_label_positions('x', self.labels[0]):
            text = Element('text', attrib={'x': x, 'y': str(self.height)})
            text.text = label
            g.append(text)
        text = Element('text', attrib={
            'x': str(int(self.width / 2)),
            'y': str(int(self.height + 40)),
            'class': 'label-title'})
        text.text = self.labels[0].text
        g.append(text)
        svg.append(g)

        g = Element('g', attrib={'class': 'labels y-labels'})
        for y, label in self.get_label_positions('y', self.labels[1]):
            text = Element('text', attrib={'x': str(self.right - 20), 'y': y})
            text.text = label
            g.append(text)
        text = Element('text', attrib={
            'x': str(self.right / 2),
            'y': str(self.height / 2),
            'class': 'label-title'})
        text.text = self.labels[1].text
        g.append(text)
        svg.append(g)
        #---
        
        points = []
        for x, y in self.points:
            h = x - self.right
            v = self.height - self.down - y
            points.append('%s, %s' % (h, v))
        points = '\n'.join(points)
        points = '\n' + points + '\n'
        g = Element('g', attrib={'class': 'main'})
        polyline = Element(
            'polyline',
            attrib={
                'fill': 'none',
                'stroke': '#0074d9',
                'stroke-width': '2',
                'points': points,
                'class': 'main',
            },
        )
        g.append(polyline)
        svg.append(g)
        style_text = tostring(style).decode('utf-8')
        svg_text = tostring(svg).decode('utf-8')
        svg_text = svg_text.replace('&#10;', '\n')  # ZMG FIXME ZZZ TODO
        return style_text + svg_text

class GraphLabel(object):

    def __init__(self, text, values, padding, include_zeroith=True):
        self.text = text
        self.values = values
        self.padding = padding
        self.include_zeroith = include_zeroith

if __name__ == '__main__':

    import webbrowser
    import pathlib
    import os

    x_labels = GraphLabel('Year', (2008, 2009, 2010, 2011, 2012), 50)
    y_labels = GraphLabel('Price', (5, 10, 14), 50, include_zeroith=False)

    lg = LineGraph('Look at This Graph',
                   height=480,
                   width=900,
                   points=[
                       (0,0),
                       (2, 3),
                       (53, 87),
                       (99, 200),
                       (444, 50),
                       (830,300)],
                   labels=[x_labels, y_labels],
    )

    # Yuck. Don't know how to get around using a file.
    path = '/tmp/.test.html'
    with open(path, 'w') as f:
        f.write(str(lg))

    uri = pathlib.Path(path).as_uri()

    webbrowser.open(uri, new=0, autoraise=True)
