from time import time
add_library("Mesh")

point_nums = [10, 50, 100, 200, 500, 1000, 5000, 10000, 20000, 50000]
for num in point_nums:
    begin = time()
    points = [(random(0, width), random(0, height)) for i in range(num)]
    v = Voronoi(points)
    print round(time() - begin, 2)
