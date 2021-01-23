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
    background(255)
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
    voronoi_regions.append(mask_polygon)
    for region in voronoi_regions:
        p = createShape()
        p.beginShape()
        [p.vertex(x, y) for x, y in region]
        p.endShape(CLOSE)
        shape(p)
        
    filetitle = "N" + str(num_points) + "S" + str(seed)
    # Add text
    fill(0)
    textSize(12)
    textAlign(CENTER)
    text(filetitle, width / 2, 15)
    noLoop()
