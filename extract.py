#!/usr/bin/env python
import sys

from html.parser import HTMLParser

def has_attr(attrs, attrname, value):
    return attrname in attrs and value in attrs[attrname].split()

td_map = [
    'time',
    'lat',
    'lon',
    'course',
    'kts',
    'mph',
    'feet',
    'rate',
    'reporting_facility'
]

class FAHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_table = False
        self.in_row = False
        self.in_td = False
        self.td_count = 0
        self.point = None
        self.points = []
        self.ignore_span = False
        
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        match tag:
            case 'table':
                if has_attr(attrs, "id", "tracklogTable"):
                    self.in_table = True

            case 'tr':
                if self.in_table:
                    if 'class' in attrs and \
                        (attrs['class'] == 'smallrow1' or \
                        attrs['class'] == 'smallrow2'):

                        self.in_row = True
                        self.td_count = -1
                        self.point = {}

            case 'td':
                if self.in_row:
                    self.td_count += 1
                    self.in_td = True

            case 'span':
                if has_attr(attrs, "class", "hide-for-medium-up"):
                    self.ignore_span = True
                    
    def handle_endtag(self, tag):
        match tag:
            case 'table':
                self.in_table = False

            case 'tr':
                if self.in_row:
                    self.in_row = False
                    self.points.append(self.point)

            case 'td':
                self.in_td = False

            case 'span':
                self.ignore_span = False

    def handle_data(self, data):
        if self.in_td and not self.ignore_span:
            field_name = td_map[self.td_count]

            match field_name:
                case 'course':
                    data = data[2:-1]
                case 'rate':
                    data = data[:-1]
                case 'reporting_facility':
                    data = data.strip()

            self.point[field_name] = data

    def get_points(self):
        return self.points

def load_file(filename):
    with open(filename) as fp:
        data = fp.read()

    return data

def convert_to_points(html):
    parser = FAHTMLParser()
    parser.feed(html)

    return parser.get_points()

def export_kml(points):
    pass

def main(argv):
    if len(argv) != 2:
        print(f"usage: {argv[0]} filename.html", file=sys.stderr)
        return 1

    filename = argv[1]

    html = load_file(filename)
    points = convert_to_points(html)
    print(points)
    export_kml(points)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
