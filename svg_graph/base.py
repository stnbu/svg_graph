# -*- mode: python; coding utf-8 -*-

from xml.etree.ElementTree import Element, tostring


class LineGraph(object):

    def __init__(self, title, points, height=400, width=600, labels=None, normalize=True):

        self.title = title
        self.height = height
        self.width = width

        if normalize:
            self._raw_points = points
            self.points = self.map_to_scale(self._raw_points)
        else:
            self.points = self._raw_points = points

        if labels is None:
            self.labels = self.make_labels()
        else:
            self.labels = labels

        self.right = self.labels[0].padding
        self.down = self.labels[1].padding

    def make_labels(self):
        num_labels = 6
        labels = []
        x_labels = []
        y_labels = []
        len_points = len(self._raw_points)
        distance = len_points / num_labels
        for l in range(0, num_labels):
            i = int(distance * l)
            x_labels.append(str(self._raw_points[i][0]))
            y_labels.append(str(self._raw_points[i][1]))
        return GraphLabel('X', x_labels, 100), GraphLabel('Y', y_labels, 100)

    def map_to_scale(self, points):
        x_min = min([x for x, _ in points])
        x_max = max([x for x, _ in points])
        y_min = min([y for _, y in points])
        y_max = max([y for _, y in points])

        _points = []
        for x, y in points:
            x_mul = 1 - (x_max - x) / (x_max - x_min)
            y_mul = 1 - (y_max - y) / (y_max - y_min)
            _points.append((x_mul * self.width, y_mul * self.height))
        return _points

    def get_label_positions(self, axis, labels_object):
        if axis == 'x':
            labels = labels_object.values
            total = self.width
            omit_index = 0
        elif axis == 'y':
            labels = list(reversed(labels_object.values))
            total = self.height
            omit_index = len(labels) - 1
        else:
            raise ValueError('do not understand axis="%s"' % axis)

        interlabel_distance = total / (len(labels) - 1)
        for i, label in enumerate(labels):
            if i == omit_index and labels_object.omit_zeroith:
                continue
            yield str(int(i * interlabel_distance)), str(label)

    def __str__(self):

        style = Element('style')
        style.text = """
        /* requires HTML5.2 */
        /* https://www.w3.org/TR/html52/document-metadata.html#the-style-element */

        /* `.main` are things we want to shift to account for labels */
        .main {
            transform: translate(%(right)spx, %(down)spx);
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
            transform: translate(%(right)spx,%(xlabels_down)spx);
        }
        .labels.y-labels {
            text-anchor: end;
            transform: translate(0px,%(down)spx);
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
            height=self.height+self.down+self.labels[0].padding,
            width=self.width+self.right+self.labels[1].padding,
            xlabels_down=self.down+20,
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

        # X axis (the horizontal line)
        g = Element('g', attrib={'class': 'axis main'})
        line_x = Element(
            'line',
            attrib={
                'x1': '0',
                'y1': str(self.height),
                'x2': str(self.width),
                'y2': str(self.height),
            },
        )
        g.append(line_x)
        svg.append(g)

        # Y axis (the vertical line)
        g = Element('g', attrib={'class': 'axis main'})
        line_y = Element(
            'line',
            attrib={
                'x1': '0',
                'y1': '0',
                'x2': '0',
                'y2': str(self.height),
            },
        )
        g.append(line_y)
        svg.append(g)

        # X axis labels
        g = Element('g', attrib={'class': 'labels x-labels'})
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

        # Y axis labels
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

        # generate a string, with newlines to represent the (x,y)'s of the `line` attribute
        points = []
        for x, y in self.points:
            h = x - self.right  # h for horizontal
            v = self.height - self.down - y  # v for vertical
            points.append('%s, %s' % (h, v))
        points = '\n'.join(points)
        points = '\n' + points + '\n'

        # Draw an actual graph line
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

        # ZZZ adding <style/> here requires HTML5.2
        # https://www.w3.org/TR/html52/document-metadata.html#the-style-element
        style_text = tostring(style).decode('utf-8')
        svg_text = tostring(svg).decode('utf-8')
        svg_text = svg_text.replace('&#10;', '\n')  # ZMG FIXME ZZZ TODO
        return style_text + svg_text


class GraphLabel(object):

    def __init__(self, text, values, padding, omit_zeroith=False):
        self.text = text
        self.values = values
        self.padding = padding
        self.omit_zeroith = omit_zeroith


if __name__ == '__main__':

    import webbrowser
    import pathlib
    import os

    x_labels = GraphLabel('Year',
                          values=(2008, 2009, 2010, 2011, 2012),
                          padding=100)
    y_labels = GraphLabel('Price',
                          values=(0, 5, 10, 15),
                          padding=100,
                          omit_zeroith=True)

    lg = LineGraph('Look at This Graph',
                   height=580,
                   width=700,
                   points=[
                       (0, 0),
                       (2, 3),
                       (53, 87),
                       (99, 200),
                       (444, 50),
                       (700, 580)],
                   labels=[x_labels, y_labels])

    # Yuck. Don't know how to get around using a file.
    path = '/tmp/.test.html'
    with open(path, 'w') as f:
        f.write(str(lg))

    uri = pathlib.Path(path).as_uri()

    webbrowser.open(uri, new=0, autoraise=True)
