# Experimenting with shapes and if they intersect with each other.
# 1. https://en.wikipedia.org/wiki/Gilbert%E2%80%93Johnson%E2%80%93Keerthi_distance_algorithm
#


class Vec3:
    def __init__(self, x, y, z):
        self._x = x
        self._y = y
        self._z = z

    def __iter__(self):
        for item in (self._x, self._y, self._z):
            yield item

    def __neg__(self):
        return Vec3(-self._x, -self._y, -self._z)

    def __repr__(self):
        return "Vec3({}, {}, {})".format(self._x, self._y, self._z)

    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z


class Cube:
    """
    Cube is defined as two points that exist in opposite diagonal corners.
    - So a Vec3(0,0,0) and a Vec3(2, 2, 2) is living in xyz space for each point:
        .
          . # note that this point is 2 units away in z
    - producing a 2 x 2 x 2 cube
    """

    def __init__(self, corner1, corner2):
        self.points = list()
        self.create_points(corner1, corner2)

    def create_points(self, corner1, corner2):
        x1, y1, z1 = corner1
        x2, y2, z2 = corner2

        # create first set of points (a side)
        self.points.append(Vec3(x1, y1, z1))
        self.points.append(Vec3(x1 + x2, y1, z1))
        self.points.append(Vec3(x1 + x2, y1 + y2, z1))
        self.points.append(Vec3(x1, y1 + y2, z1))

        # create second set of points
        self.points.append(Vec3(x2, y2, z2))
        self.points.append(Vec3(x2 + x1, y2, z2))
        self.points.append(Vec3(x2 + x1, y2 + y1, z2))
        self.points.append(Vec3(x2, y2 + y1, z2))


def dot_product(a, b):
    return a.x * b.x + a.y * b.y + a.z * b.z


def support(shape, direction):
    """
    Support(shape, d), which returns the point on shape which has the highest dot product with d.
    :param shape:
    :param direction:
    :return:
    """
    furthest_in_direction = None
    result = -1_000_000_000
    for point in shape.points:
        product = point.x * direction.x + point.y * direction.y + point.z * direction.z
        if product > result:
            result = product
            furthest_in_direction = point

    return furthest_in_direction


def NearestSimplex(s):
    pass


def gjk_intersection(p, q, initial_axis):
    """
    Collision detection alogrithm named after Gilbert Johnson Keerthi.
    :param p: Shape
    :param q: Shape
    :param initial_axis: Vec3
    :return:
    """
    # a -> Vec3
    # s -> list(): Simplex result
    # d -> Vec3 - Direction

    a = support(p, initial_axis) - support(q, -initial_axis)
    s = [a]
    d = -a

    while True:
        a = support(p, d) - support(q, -d)

        if dot_product(a, d) < 0:
            # reject - we are already moving away from origin.
            return False

        s.append(a)
        print(s)
        break

        # s, d, contains_origin = NearestSimplex(s)
        # if contains_origin:
        #    accept
        #


if __name__ == "__main__":
    corner1 = Vec3(0.0, 0.0, 0.0)
    corner2 = Vec3(1.0, 1.0, 1.0)

    direction = Vec3(0.0, 0.0, 1.0)
    print("[Direction]: {} and its negative: {}".format(direction, -direction))

    cube_01 = Cube(corner1, corner2)
    cube_02 = Cube(corner1, Vec3(2.0, 2.0, 2.0))

    i = support(cube_01, direction)
    print("[Cube_01] Highest Dot Product Point (+ direction): {}".format(i))

    j = support(cube_02, -direction)
    print("[Cube_02] Highest Dot Product Point (- direction): {}".format(j))

    gjk_intersection(cube_01, cube_02, direction)
