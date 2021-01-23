from time import time
add_library("ToxicLibs")

point_nums = [10, 50, 100, 200, 500, 1000, 5000, 10000]
for num in point_nums:
    begin = time()
    points = [Vec2D(random(0, width), random(0, height)) for i in range(num)]
    v = Voronoi()
    v.addPoints(points)
    print round(time() - begin, 2)
