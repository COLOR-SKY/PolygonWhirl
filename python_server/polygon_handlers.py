"""
Author: colorsky
Date: 2020/01/15
"""

from multiprocessing import Pool, cpu_count
from shapely.geometry import Polygon, Point
import numpy as np
import random


def polygon_simplify(points, tolerance):
    coords = Polygon(points).simplify(tolerance).exterior.coords
    if not coords:
        return
    x, y = coords.xy
    p = list(zip(x, y))
    if len(p) < 2:
        return
    return p


def polygon_interpolate(polygon: list,
                        displacement_f: float = None,
                        displacement: float = 10,
                        min_area: float = 10,
                        max_iter: int = 100):
    """Recursively interpolate polygon segments to generate a whirl like output.

    :param polygon: Vertices of the polygon
    :param displacement_f: Factor of how much distance the new point moves along the edge relative to the edge's length
    :param displacement: Displacement of each of the new points relative to the previous points
    :param min_area: Minimum area to terminate the interpolation
    :param max_iter: Maximum iterations to terminate the interpolation
    :return: {iter_0:polygon, iter_1:polygon, ..., max_iter:polygon}
    """
    output = {0: polygon}
    if displacement == 0:
        return output
    if polygon[0] != polygon[-1]:  # Ensure the polygon is closed
        polygon.append(polygon[0])

    # Begin interpolating
    parent_polygon = polygon
    for iteration in range(1, max_iter + 1):
        if Polygon(parent_polygon).area < min_area:
            break
        child_polygon = []
        for i in range(len(parent_polygon) - 1):
            displacement_ = float(displacement)
            pi = np.array(parent_polygon[i])
            pj = np.array(parent_polygon[i + 1])
            if all(pi == pj):
                continue
            v = pj - pi
            dist = np.sqrt(np.sum(v ** 2))
            normalized_v = v / dist
            if displacement_f:
                displacement_ = dist * displacement_f
            qi = pi + normalized_v * displacement_
            if dist <= displacement_:
                qi = pi
            child_polygon += [qi.tolist()]
        if child_polygon[0] != child_polygon[-1]:  # Ensure the polygon is closed
            child_polygon.append(child_polygon[0])
        simplify_depth = 1
        while len(child_polygon) > 12:
            # new_polygon = polygon_simplify_curve_edge(new_polygon)
            child_polygon = polygon_simplify(child_polygon, simplify_depth)
            simplify_depth += 1
        if Polygon(parent_polygon).area <= Polygon(child_polygon).area:
            break
        output[len(output)] = child_polygon
        parent_polygon = child_polygon
    return output


def polygons_interpolate_wrapper(*args):
    points, kwargs = args[0]
    return polygon_interpolate(polygon=points, **kwargs)


def polygons_interpolate(polygons, **kwargs):
    if len(polygons) < 10:
        return [polygons_interpolate_wrapper((polygon, kwargs)) for polygon in polygons]
    else:
        # multiprocessing
        with Pool(cpu_count() - 1) as pool:
            args = [[polygon, kwargs] for polygon in polygons]
            output = pool.map(polygons_interpolate_wrapper, args)
        return output


def random_points_inside_polygon(polygon: list, n: int, seed: int = -1):
    """
    Generate n random points inside the polygon with random seed set to seed(if provided).

    :param polygon: Vertices of the polygon.
    :param n: Number of random points to generate.
    :param seed: Random seed.
    :return: A list of points
    """
    if seed >= 0:
        random.seed(seed)
    polygon = Polygon(polygon)
    minx, miny, maxx, maxy = polygon.bounds
    points = []
    for i in range(n):
        x, y = random.uniform(minx, maxx), random.uniform(miny, maxy)
        while not polygon.contains(Point(x, y)):
            x, y = random.uniform(minx, maxx), random.uniform(miny, maxy)
        points.append([x, y])
    return points
