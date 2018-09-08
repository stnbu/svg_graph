# -*- mode: python; coding utf-8 -*-

from xml.etree.ElementTree import Element, tostring


class LineGraph(object):

    def __init__(self, title, points, height=400, width=600, normalize=True):
        self.title = title
        self.height = height
        self.width = width
        points = list(points)  # we should be dealing with smallish data sets.
        self.points = self.normalize(points)

    def normalize(self, points):
        x_min = min([x for x, _ in points])
        x_max = max([x for x, _ in points])
        y_min = min([y for _, y in points])
        y_max = max([y for _, y in points])
        for point in points:
            x, y = point
            x_mul = 1 - (x_max - x) / (x_max - x_min)
            y_mul = 1 - (y_max - y) / (y_max - y_min)
            # it's likely (enough?) converting to int here is cheaper than doing it in the browser, etc.
            yield int(x_mul * self.width), int(y_mul * self.height)

    def to_xml(self):

        style = Element('style')  # but how "<style scoped>"?
        style.text = """
        /* requires HTML5.2 */
        /* https://www.w3.org/TR/html52/document-metadata.html#the-style-element */

        /* `.main` are things we want to shift to account for labels */
        /*
        .main {
            transform: translate(Xpx, Ypx);
        }
        */
        .graph {
            height: %(height)spx;
            width: %(width)spx;
        }
        .axis {
            stroke: #ccc;
            stroke-dasharray: 0;
            stroke-width: 1;
        }
        """ % dict(
            height=self.height,
            width=self.width,
        )

        svg = Element(
            'svg',
            attrib={
                'version': '1.2',
                'xmlns': 'http://www.w3.org/2000/svg',
                'xmlns:xlink': 'http://www.w3.org/1999/xlink',
                'class': 'graph',
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

        # generate a string, with newlines to represent the (x,y)'s of the `line` attribute
        points = []
        for x, y in self.points:
            h = x  # h for horizontal
            v = self.height - y  # v for vertical
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

if __name__ == '__main__':

    import webbrowser
    import pathlib
    import os

    lg = LineGraph('Look at This Graph',
                   height=580,
                   width=700,
                   points=[
                       (0, 0),
                       (2, 3),
                       (53, 87),
                       (99, 200),
                       (444, 50),
                       (700, 580)])

    # Yuck. Don't know how to get around using a file.
    path = '/tmp/.test.html'
    with open(path, 'w') as f:
        f.write(str(lg))

    uri = pathlib.Path(path).as_uri()

    webbrowser.open(uri, new=0, autoraise=True)
