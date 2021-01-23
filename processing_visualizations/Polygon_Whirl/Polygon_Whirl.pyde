"""
Author: colorsky
Date: 2020/01/19
"""

import sys
import math
# Replace with your environment dir
sys.path.append('/Python Project/venv_2.7/lib/python2.7/site-packages/')
import requests

def circle_points(r, n, xoff=0, yoff=0):
    return [(math.cos(2 * math.pi / n * x) * r + xoff, math.sin(2 * math.pi / n * x) * r + yoff) for x in range(0, n)]

def setup():
    size(800, 800)

def draw():
    background(240)
    rows, cols = 4, 4
    polygons = []
    for r in range(rows):
        for c in range(cols):
            xoff = width / (cols + 1) * (c + 1)
            yoff = height / (rows + 1) * (r + 1)
            polygons.append(circle_points(60, (rows * r + c + 3), xoff, yoff))

    data = {
        "polygons": polygons,
        "displacement_f": 0.1,
        "min_area": 5,
        "max_iter": 150
    }
    api = "http://127.0.0.1:5699/PolygonsInterpolate"
    interpolations = requests.post(api, json=data).json()

    noFill()
    for interpolated in interpolations:
        for iteration in interpolated:
            strokeWeight(map(int(iteration), 0, len(interpolated), 1, 0))
            polygon = interpolated[iteration]
            p = createShape()
            p.beginShape()
            for x, y in polygon:
                p.vertex(x, y)
            p.endShape(CLOSE)
            shape(p)
    noLoop()
