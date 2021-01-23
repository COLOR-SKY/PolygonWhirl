from scipy.spatial import Voronoi
from time import time
from random import randint

point_nums = [10, 50, 100, 200, 500, 1000, 5000, 10000, 20000, 50000, 100000]
for num in point_nums:
    begin = time()
    points = [(randint(0, 100), randint(0, 100)) for i in range(num)]
    v = Voronoi(points)
    print(round(time() - begin, 2))
