"""
Author: colorsky
Date: 2020/01/15
"""

from scipy.spatial import Voronoi
from scipy.spatial.qhull import QhullError
from shapely.geometry import Polygon
import numpy as np


def get_clipped_voronoi(polygon: list, points: list):
    """
    Generate regions of voronoi diagram clipped by the polygon.

    :param polygon: Vertices of the polygon.
    :param points: Coordinates of points to construct a convex hull from
    :return: A list of voronoi diagram region's vertices
    """
    minx, miny, maxx, maxy = Polygon(polygon).bounds  # Add mask's boundary
    points += [[minx - 1000, miny - 1000], [maxx + 1000, miny - 1000],
               [maxx + 1000, maxy + 1000], [minx - 1000, maxy + 1000]]
    try:
        voronoi = Voronoi(points)
    except QhullError:
        return []

    regions = [voronoi.vertices[region_idxes] for region_idxes in voronoi.regions if
               -1 not in region_idxes and len(region_idxes) > 2]

    # Clip regions
    clipped_regions = []
    for region in regions:
        clipped_region = None
        if Polygon(polygon).contains(Polygon(region)):
            clipped_region = region.tolist()
        else:
            intersection = Polygon(region).intersection(Polygon(polygon))
            if type(intersection) is not Polygon:
                continue
            intersection = (np.array(intersection.exterior.coords)).tolist()
            if len(intersection) > 2:
                clipped_region = intersection
        if clipped_region:
            clipped_regions.append(clipped_region)
    return clipped_regions
