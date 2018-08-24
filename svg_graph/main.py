# -*- mode: python; coding utf-8 -*-

from xml.etree.ElementTree import Element, tostring


class LineGraph(object):

    def __init__(self, title, height, width, points, labels):

        self.title = title

        self.height = height
        self.width = width
        self.labels = labels
        self.points = points

        self.right = 0
        self.down = 0

    def get_label_positions(self, axis):
        if axis == 'x':
            labels = self.labels[0][1]
            total = self.width
        elif axis == 'y':
            labels = list(reversed(self.labels[1][1]))
            total = self.height
        else:
            raise ValueError('do not understand axis="%s"' % axis)

        interlabel_distance = total / (len(labels) - 1)
        for i, label in enumerate(labels):
            if label is None:
                continue
            yield str(int(i * interlabel_distance)), str(label)

    def __str__(self):

        style = Element('style')
        style.text = """
            /* requires HTML5.2 */
            /* https://www.w3.org/TR/html52/document-metadata.html#the-style-element */
            .graph {
                transform: translate(%(right)spx, %(down)spx);
                height: %(height)spx;
                width: %(width)spx;
            }
            .axis {
                stroke: #ccc;
                stroke-dasharray: 0;
                stroke-width: 1;
            }
            .data {
                fill: red;
                stroke-width: 1;
            }
        """ % dict(
            right=self.right,
            down=self.down,
            height=self.height+self.down,
            width=self.width+self.right,
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

        g = Element('g', attrib={'class': 'axis'})
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

        g = Element('g', attrib={'class': 'axis'})
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

        points = []
        for x, y in self.points:
            h = x - self.right
            v = self.height - self.down - y
            points.append('%s, %s' % (h, v))
        points = '\n'.join(points)
        points = '\n' + points + '\n'
        g = Element('g', attrib={'class': 'graph'})
        polyline = Element(
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
        style_text = tostring(style).decode('utf-8')
        svg_text = tostring(svg).decode('utf-8')
        svg_text = svg_text.replace('&#10;', '\n')  # ZMG FIXME ZZZ TODO
        return style_text + svg_text

if __name__ == '__main__':

    import webbrowser
    import pathlib
    import os

    from tests import top, bottom

    lg = LineGraph('Look at This Graph',
                   height=480,
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
