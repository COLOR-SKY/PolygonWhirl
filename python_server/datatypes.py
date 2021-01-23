from pydantic import BaseModel
from typing import List


class PolygonsInterpolateData(BaseModel):
    polygons: List[list]
    displacement_f: float = None
    displacement: float = 10
    min_area: float = 10
    max_iter: int = 100


class RandomPointsInsidePolygonData(BaseModel):
    polygon: List[list]
    n: int = None
    seed: int = -1


class ClippedVoronoiData(BaseModel):
    polygon: List[list]
    points: list

