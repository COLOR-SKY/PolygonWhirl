"""
Author: colorsky
Date: 2020/01/20
"""

import sys
# Replace with your environment dir
sys.path.append('/Python Project/venv_2.7/lib/python2.7/site-packages/')
import requests

def setup():
    size(800, 800)

def draw():
    background(0)
    noFill()
    num_points = 10
    seed = 999
    mask_polygon = [[20, 20], [width - 20, 20],
                    [width - 20, height - 20], [20, height - 20]]
    baseapi = "http://127.0.0.1:5699"
    points = requests.post(baseapi + "/RandomPointsInsidePolygon", json={
        "polygon": mask_polygon,
        "n": 10,
        "seed": 10
    }).json()
    voronoi_regions = requests.post(baseapi + "/ClippedVoronoi", json={
        "polygon": mask_polygon,
        "points": points
    }).json()
    interpolations = requests.post(baseapi + "/PolygonsInterpolate", json={
        "polygons": voronoi_regions,
        "displacement": 1,
        "min_area": 5,
        "max_iter": 1000
    }).json()
    for interpolated in interpolations:
        for iteration in interpolated:
            stroke(map(int(iteration), 0, len(interpolated), 255, 0))
            strokeWeight(0.3)
            polygon = interpolated[iteration]
            p = createShape()
            p.beginShape()
            for x, y in polygon:
                p.vertex(x, y)
            p.endShape(CLOSE)
            shape(p)

    filetitle = "N" + str(num_points) + "S" + str(seed)
    # Add text
    fill(255)
    textSize(12)
    textAlign(CENTER)
    text(filetitle, width / 2, 15)
    noLoop()
